#include <string.h> // for basename(3) that doesn't modify its argument
#include <unistd.h> // for getopt
#include <sstream>

#include "cam_properties.hpp"

#include "apriltags.hpp"
#include "undistort.hpp"

#include <nlohmann/json.hpp>

#include "mqtt/client.h"

#include <opencv2/opencv.hpp> // For OpenCV functions
#include <opencv2/imgcodecs.hpp> // For image encoding
#include <base64.h> // Ensure you have this library or an equivalent for base64 encoding

// for convenience
using json = nlohmann::basic_json<std::map, std::vector, std::string, bool, std::int64_t, std::uint64_t, float>;

json jsonify_tag(nvAprilTagsID_t detection)
{
    // create an empty structure (null)
    json j;

    j["id"] = detection.id;

    j["pos"]["x"] = detection.translation[0];
    j["pos"]["y"] = detection.translation[1];
    j["pos"]["z"] = detection.translation[2];

    j["rotation"] = {{detection.orientation[0], detection.orientation[3], detection.orientation[6]},
                     {detection.orientation[1], detection.orientation[4], detection.orientation[7]},
                     {detection.orientation[2], detection.orientation[5], detection.orientation[8]}};

    return j;
}

int main()
{
    // MQTT setup
    const std::string SERVER_ADDRESS{"tcp://mqtt:18830"};
    const std::string CLIENT_ID{"nvapriltags"};
    const std::string TAG_TOPIC{"avr/apriltags/raw"};
    const std::string FPS_TOPIC{"avr/apriltags/fps"};
    const std::string CAMFEED_TOPIC{"avr/apriltag/camfeed"};

    const int QOS = 0;
    mqtt::client client(SERVER_ADDRESS, CLIENT_ID);
    mqtt::connect_options connOpts;
    connOpts.set_keep_alive_interval(20);
    connOpts.set_clean_session(true);

    try {
        std::cout << "\nConnecting..." << std::endl;
        client.connect(connOpts);
        std::cout << "...OK" << std::endl;
    } catch (const mqtt::exception &exc) {
        std::cerr << exc.what() << std::endl;
        return 1;
    }

    // Video capture setup
    cv::VideoCapture capture("nvarguscamerasrc ! video/x-raw(memory:NVMM), width=1280, height=720,format=NV12, framerate=15/1 ! nvvidconv ! video/x-raw,format=BGRx !  videoconvert ! videorate ! video/x-raw,format=BGR,framerate=5/1 ! appsink", cv::CAP_GSTREAMER);
    std::cout << "made it past cap device" << std::endl;

    cv::Mat frame;
    cv::Mat img_rgba8;

    capture.read(frame);
    cv::cvtColor(frame, img_rgba8, cv::COLOR_BGR2RGBA);
    setup_vpi(img_rgba8);

    // AprilTags handler setup
    auto *impl_ = new AprilTagsImpl();
    impl_->initialize(img_rgba8.cols, img_rgba8.rows,
                      img_rgba8.total() * img_rgba8.elemSize(), img_rgba8.step,
                      fx, fy, ppx, ppy, //camera params
                      0.174,            //tag edge length
                      6);               //max number of tags

    while (capture.isOpened())
    {
        auto start = std::chrono::system_clock::now();

        if (capture.read(frame))
        {
            undistort_frame(frame);
            cv::cvtColor(frame, img_rgba8, cv::COLOR_BGR2RGBA);

            uint32_t num_detections = process_frame(img_rgba8, impl_);

            std::vector<uchar> buffer;
            cv::imencode(".jpg", img_rgba8, buffer);
            std::string encoded = base64::encode(buffer.data(), buffer.size());

            json camfeed_json;
            camfeed_json["image"] = encoded;

            std::string camfeed_payload = camfeed_json.dump();
            client.publish(CAMFEED_TOPIC, camfeed_payload.c_str(), camfeed_payload.length(), QOS);

            // Process detections and publish as before
            // ...
        }
    }

    delete impl_;
    return 0;
}

// while(capture.isOpened())
// {
//     std::cout<<"while"<<std::endl;
//     capture.read(frame);
//     cv::namedWindow("frame", 0);
//     cv::resizeWindow("frame", 1280,720);
//     cv::imshow("frame", frame);
//     if (cv::waitKey(1)==27)
//         break;
// }
