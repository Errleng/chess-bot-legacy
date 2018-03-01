#include <iostream>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>

double rgbTemplateMatchPath(std::string imagePath, std::string templatePath) {
    cv::Mat result;
    double minVal, maxVal;
    cv::Point minLoc, maxLoc;

    cv::Mat temp = cv::imread(templatePath, 1);
    cv::Mat image = cv::imread(imagePath, 1);

    int result_rows = image.rows - temp.rows + 1;
    int result_cols = image.cols - temp.cols + 1;

    result.create(result_rows, result_cols, CV_32FC1);
    cv::matchTemplate(image, temp, result, cv::TM_CCOEFF_NORMED);
    cv::minMaxLoc(result, &minVal, &maxVal, &minLoc, &maxLoc);

    return maxVal;
}

double rgbTemplateMatchImage(cv::Mat image, cv::Mat temp) {
    cv::Mat result;
    double minVal, maxVal;
    cv::Point minLoc, maxLoc;

    int result_rows = image.rows - temp.rows + 1;
    int result_cols = image.cols - temp.cols + 1;

    result.create(result_rows, result_cols, CV_32FC1);
    cv::matchTemplate(image, temp, result, cv::TM_CCOEFF_NORMED);
    cv::minMaxLoc(result, &minVal, &maxVal, &minLoc, &maxLoc);

    return maxVal;
}

int main() {
    std::cout << "Start Program" << std::endl;

    std::cout << "\nSetup started" << std::endl;

    std::string IMAGES_PATH = "D:\\Documents\\SourceTree\\ChessBot\\Screenshots\\";
    int boardDimension = 508;
    int pieceDimension = 508/4;
    int boardCropRect[4] = {160, 155, 690, 660};
    int boardSideSquareCount = 8;

    bool whiteCastleKingSide = true;
    bool whiteCastleQueenSide = true;

    bool blackCastleKingSide = true;
    bool blackCastleQueenSide = true;

    int gameMove = 0;
    int accuracy = 0;
    int difficulty = 0;

    std::string templates[24];

    std::cout << "\nSetup ended" << std::endl;

    cv::Mat image = cv::imread(IMAGES_PATH + "ChessShot" + ".jpg", 1);
    cv::imshow("Chess Screenshot", image);
    cv::waitKey(0);

    std::cout << "End Program" << std::endl;
    return 0;
}