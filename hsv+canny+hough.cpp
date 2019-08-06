// 从摄像头中读取
#include <opencv2/opencv.hpp>
#include <opencv2/core.hpp>
#include <opencv2//highgui/highgui.hpp>
#include <iostream>

int main() {
    cv::namedWindow("暴风影音", cv::WINDOW_AUTOSIZE);
    
    cv::VideoCapture cap;
    // 读取摄像头
    cap.open(0);
    // 判断摄像头是否打开
    if (!cap.isOpened()) {
        std::cerr << "Could't open capture" << std::endl;
        return -1;
    }
    cv::Mat frame;
    // 接收键盘上的输入
    char keyCode;
    // 保存的图片名称
    std::string imgName = "123.jpg";
    while (1) {
        // 把读取的摄像头传入Mat对象中
        cap >> frame;
        // 判断是否成功
        if (frame.empty()) {
            break;
        }
        // 把每一帧图片表示出来
        cv::imshow("暴风影音", frame);
        // 在30毫秒内等待是否存在键盘输入
        keyCode = cv::waitKey(30);
        if (keyCode == 's') {
            // 把图片保存起来
            cv::imwrite(imgName, frame);
            imgName.at(0)++;
            frame.release();
        } else if (keyCode == 27) {
            break;
        }
    }
    return 0;
}

