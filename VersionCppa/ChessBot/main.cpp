#include <QtCore>
#include <iostream>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>

#include <windows.h>
#include <chrono>

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

cv::Mat matScreenShot(POINT a, POINT b)
{
    int width = abs(a.x - b.x);
    int height = abs(a.y - b.y);

    HBITMAP hBitmap; // <-- The image represented by hBitmap
    cv::Mat matBitmap; // <-- The image represented by mat


    // Initialize DCs
    HDC hdcSys = GetDC(NULL); // Get DC of the target capture..
    HDC hdcMem = CreateCompatibleDC(hdcSys); // Create compatible DC




    void *ptrBitmapPixels; // <-- Pointer variable that will contain the pointer for the pixels




    // Create hBitmap with Pointer to the pixels of the Bitmap
    BITMAPINFO bi; HDC hdc;
    ZeroMemory(&bi, sizeof(BITMAPINFO));
    bi.bmiHeader.biSize = sizeof(BITMAPINFOHEADER);
    bi.bmiHeader.biWidth = width;
    bi.bmiHeader.biHeight = -height;  //negative so (0,0) is at top left
    bi.bmiHeader.biPlanes = 1;
    bi.bmiHeader.biBitCount = 32;
    hdc = GetDC(NULL);
    hBitmap = CreateDIBSection(hdc, &bi, DIB_RGB_COLORS, &ptrBitmapPixels, NULL, 0);
    // ^^ The output: hBitmap & ptrBitmapPixels


    // Set hBitmap in the hdcMem
    SelectObject(hdcMem, hBitmap);



    // Set matBitmap to point to the pixels of the hBitmap
    matBitmap = cv::Mat(height, width, CV_8UC3, ptrBitmapPixels, 0);
    //              ^^ note: first it is y, then it is x. very confusing

    // * SETUP DONE *




    // Now update the pixels using BitBlt
    BitBlt(hdcMem, 0, 0, width, height, hdcSys, 0, 0, SRCCOPY);
    DeleteDC(hdcMem);
    ReleaseDC(NULL, hdcSys);
//    DeleteObject(hBitmap);
    return matBitmap;
}

int main() {
    std::cout << "Start Program" << std::endl;
    std::chrono::high_resolution_clock::time_point t1 = std::chrono::high_resolution_clock::now();

    std::cout << "\nSetup Started" << std::endl;

    const bool newBoard = false;

    const std::string ENGINES_PATH = "D:\\Documents\\SourceTree\\Chessbot\\Engines\\";
    const std::string stockfishPath = "stockfish-9-win\\Windows\\stockfish_9_x64.exe";

    const std::string IMAGES_PATH = "D:\\Documents\\SourceTree\\ChessBot\\Screenshots\\";
    const std::string TEMPLATES_PATH = IMAGES_PATH + "Pieces\\";
    const std::string SAVE_PATH = IMAGES_PATH + "TempIconOutput\\";
    const std::string imageFileType = ".png";

    const int boardDimension = 808;
    const int pieceDimension = 808/8;
    const int boardCropRect[4] = {284, 162, 1092, 970};
    const int boardSideSquareCount = 8;

    bool whiteCastleKingSide = true;
    bool whiteCastleQueenSide = true;

    bool blackCastleKingSide = true;
    bool blackCastleQueenSide = true;

    int gameMove = 0;
    int accuracy = 0;
    int difficulty = 0;

    const int templateCount = 12;
    std::tuple<int, int> templates[templateCount];

    std::tuple<int, int> blackRooks (1, 8);
    std::tuple<int, int> blackKnights (2, 7);
    std::tuple<int, int> blackBishops (3, 6);
    std::tuple<int, int> blackPawns (9, 10);
    std::tuple<int, int> blackQueens (4, 11);
    std::tuple<int, int> blackKings (5, 12);

    std::tuple<int, int> whiteQueens (53, 60);
    std::tuple<int, int> whiteKings (54, 61);
    std::tuple<int, int> whitePawns (55, 56);
    std::tuple<int, int> whiteRooks (57, 64);
    std::tuple<int, int> whiteKnights (58, 63);
    std::tuple<int, int> whiteBishops (59, 62);

    templates[0] = blackPawns;
    templates[1] = whitePawns;
    templates[2] = blackRooks;
    templates[3] = whiteRooks;
    templates[4] = blackKings;
    templates[5] = whiteKings;
    templates[6] = blackQueens;
    templates[7] = whiteQueens;
    templates[8] = blackBishops;
    templates[9] = whiteBishops;
    templates[10] = blackKnights;
    templates[11] = whiteKnights;

    std::string pieceFEN[templateCount] = {"p", "P", "r", "R", "k", "K", "q", "Q", "b", "B", "n", "N"};

    for (int i = 0; i < sizeof(templates)/sizeof(templates[0]); i++) {
        std::cout << std::get<0>(templates[i]) << " " << std::get<1>(templates[i]) << std::endl;
    }
    cv::Mat templateMats[templateCount * 2];
    if (!newBoard) {
        for (int tuple = 0; tuple < templateCount; tuple++) {
            int firstTemplate = std::get<0>(templates[tuple]);
            int secondTemplate = std::get<1>(templates[tuple]);
            cv::Mat templateMat = cv::imread(TEMPLATES_PATH + std::to_string(firstTemplate) + imageFileType, -1);
            cv::cvtColor(templateMat, templateMat, CV_BGR2BGRA);
            templateMats[tuple * 2] = templateMat;
            templateMat = cv::imread(TEMPLATES_PATH + std::to_string(secondTemplate) + imageFileType, -1);
            cv::cvtColor(templateMat, templateMat, CV_BGR2BGRA);
            templateMats[tuple * 2 + 1] = templateMat;
        }
    }

//    for (int i = 0; i < sizeof(templateMats)/sizeof(templateMats[0]); i++) {
//        cv::imshow("Template", templateMats[i]);
//        cv::waitKey(500);
//    }

    std::cout << "\nSetup Ended" << std::endl;


    POINT a, b;
    a.x = boardCropRect[0];
    a.y = boardCropRect[1];
    b.x = boardCropRect[2];
    b.y = boardCropRect[3];
    int width = abs(a.x - b.x);
    int height = abs(a.y - b.y);

    int counter = 0;
    while (counter < 1) {
        HBITMAP hBitmap; // <-- The image represented by hBitmap
        cv::Mat matBitmap; // <-- The image represented by mat


        // Initialize DCs
        HDC hdcSys = GetDC(NULL); // Get DC of the target capture..
        HDC hdcMem = CreateCompatibleDC(hdcSys); // Create compatible DC

        void *ptrBitmapPixels; // <-- Pointer variable that will contain the pointer for the pixels

        // Create hBitmap with Pointer to the pixels of the Bitmap
        BITMAPINFO bi; HDC hdc;
        ZeroMemory(&bi, sizeof(BITMAPINFO));
        bi.bmiHeader.biSize = sizeof(BITMAPINFOHEADER);
        bi.bmiHeader.biWidth = width;
        bi.bmiHeader.biHeight = -height;  //negative so (0,0) is at top left
        bi.bmiHeader.biPlanes = 1;
        bi.bmiHeader.biBitCount = 32;
        hdc = GetDC(NULL);
        hBitmap = CreateDIBSection(hdc, &bi, DIB_RGB_COLORS, &ptrBitmapPixels, NULL, 0);
        // ^^ The output: hBitmap & ptrBitmapPixels


        // Set hBitmap in the hdcMem
        SelectObject(hdcMem, hBitmap);



        // Set matBitmap to point to the pixels of the hBitmap
        matBitmap = cv::Mat(height, width, CV_8UC4, ptrBitmapPixels, 0);
        //              ^^ note: first it is y, then it is x. very confusing

        // * SETUP DONE *

        // Now update the pixels using BitBlt
        BitBlt(hdcMem, 0, 0, width, height, hdcSys, a.x, a.y, SRCCOPY);

        if (newBoard) {
            std::cout << "rows: " << matBitmap.rows << " cols: " << matBitmap.cols << std::endl;
            cv::imshow("Screenshot", matBitmap);
            cv::waitKey(500);

            int imageNumber = 0;
            for (int row = 1; row <= boardSideSquareCount; row++) {
                for (int col = 1; col <= boardSideSquareCount; col++) {
                    imageNumber++;
                    cv::Rect ROI(pieceDimension * (col-1), pieceDimension * (row-1), pieceDimension, pieceDimension);
                    cv::Mat pieceImage = matBitmap(ROI);
                    cv::imwrite(SAVE_PATH + std::to_string(imageNumber) + imageFileType, pieceImage);
                    cv::imshow("Piece", pieceImage);
                    cv::waitKey(250);
                }
            }
        }

        std::string sideToMove = "w";

        std::string FEN = "";

        int emptySquareCount = 0;
        int rowSlashCount = 0;

        for (int row = 1; row <= boardSideSquareCount; row++) {
            for (int col = 1; col <= boardSideSquareCount; col++) {
                cv::Rect ROI(pieceDimension * (col-1), pieceDimension * (row-1), pieceDimension, pieceDimension);
                cv::Mat pieceImage = matBitmap(ROI);

                bool matchedTemplate = false;

                for (int i = 0; i < sizeof(templateMats)/sizeof(templateMats[0]); i++) {
                    double similarity = rgbTemplateMatchImage(pieceImage, templateMats[i]);
                    if (similarity > 0.8) {
                        if (emptySquareCount > 0) {
                            FEN += std::to_string(emptySquareCount);
                            emptySquareCount = 0;
                        }
                        FEN += pieceFEN[i/2];
                        matchedTemplate = true;
                        break;
                    }
                }

                if (!matchedTemplate) {
                    emptySquareCount += 1;
                }
                rowSlashCount += 1;
                if (rowSlashCount >= 8 && !(col == 8 && row == 8)) {
                    if (emptySquareCount > 0) {
                        FEN += std::to_string(emptySquareCount);
                        emptySquareCount = 0;
                    }
                    FEN += "/";
                    rowSlashCount = 0;
                }
            }
        }

        std::cout << "FEN: " << FEN << std::endl;

        std::string castleFEN = "";
        if (whiteCastleKingSide)
            castleFEN += "K";
        if (whiteCastleQueenSide)
            castleFEN += "Q";
        if (blackCastleKingSide)
            castleFEN += "k";
        if (blackCastleQueenSide)
            castleFEN += "q";

        if (castleFEN == "")
            castleFEN = "-";

        std::string formattedFen = FEN + " " + sideToMove + " " + castleFEN + " - " + "0 0";

        DeleteDC(hdcMem);
        ReleaseDC(NULL, hdcSys);
        DeleteObject(hBitmap);

//        QProcess exe;
//        QString stockfish = QString::fromStdString(ENGINES_PATH + stockfishPath);
//        exe.start(stockfish);
//        exe.write("uci");
//        QString engineResponse = exe.readAllStandardOutput();
//        std::string strResponse = engineResponse.toStdString();
//        std::cout << "Engine Response: " << strResponse << std::endl;

        counter++;
    }


    std::chrono::high_resolution_clock::time_point t2 = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(t2 - t1).count();

    std::cout << "End Program" << std::endl;
    std::cout << "Duration of program is " << duration << " milliseconds" << std::endl;
    return 0;
}