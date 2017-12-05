// ChessBot.cpp : Defines the entry point for the application.
//

#include "stdafx.h"
#include "ChessBot.h"

#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>

#include <Ole2.h>
#include <OleCtl.h>

#include <filesystem>

#include <iostream>
#include <fstream>

using namespace std;
using namespace cv;

namespace fs = experimental::filesystem;

#define MAX_LOADSTRING 100

// Global Variables:
HINSTANCE hInst;                                // current instance
WCHAR szTitle[MAX_LOADSTRING];                  // The title bar text
WCHAR szWindowClass[MAX_LOADSTRING];            // the main window class name


//--------------------//
#define IDT_TEXTSECOND 101

BOOL RUNBOT = FALSE;
BOOL COLOR;
BOOL WHITE = true;
BOOL BLACK = false;

string SAVE_PATH = "D:\\Documents\\SourceTree\\ChessBot\\Screenshots\\";
string enginePath = "C:\\Users\\aisae\\Desktop\\Engines\\";
string screenShots[24] = {"BPawnB", "BPawnW", "WPawnB", "WPawnW", "BRookB", "BRookW", "WRookB", "WRookW", "BBishopB", "BBishopW", "WBishopB", "WBishopW", "BNnightB", "BNnightW", "WNnightB", "WNnightW", "BKingB", "BKingW", "WKingB", "WKingW", "BQueenB", "BQueenW", "WQueenB", "WQueenW"};

HWND Windows[10];

float boardSide = 504;
float pieceSide = boardSide / 8;

int sideArray[8] = { 1,2,3,4,5,6,7,8 };
//--------------------//

double rgbTemplateMatch(string tempPath, Mat img)
{
	/// Source image to display
	Mat img_display;
	Mat templ = imread(tempPath, CV_LOAD_IMAGE_COLOR);

	//imshow("temp", templ);
	//waitKey(0);

	Mat result;

	img.copyTo(img_display);

	/// Create the result matrix
	int result_cols = img.cols - templ.cols + 1;
	int result_rows = img.rows - templ.rows + 1;

	result.create(result_cols, result_rows, CV_32FC1);

	/// Do the Matching and Normalize

	cvtColor(img, img, CV_BGR2RGB);
	//cvtColor(templ, templ, CV_BGR2RGB);
	
	//imshow("templRGB", templ);
	//waitKey(0);

	//imshow("imgRGB", img);
	//waitKey(0);

	matchTemplate(img, templ, result, TM_CCOEFF_NORMED);
	//normalize(result, result, 0, 1, NORM_MINMAX, -1, Mat());

	/// Localizing the best match with minMaxLoc
	double minVal; double maxVal; Point minLoc; Point maxLoc;

	minMaxLoc(result, &minVal, &maxVal, &minLoc, &maxLoc, Mat());

	/// For SQDIFF and SQDIFF_NORMED, the best matches are lower values. For all the other methods, the higher the better

	/// Show me what you got
	//rectangle(img_display, matchLoc, Point(matchLoc.x + templ.cols, matchLoc.y + templ.rows), Scalar::all(0), 2, 8, 0);
	//rectangle(result, matchLoc, Point(matchLoc.x + templ.cols, matchLoc.y + templ.rows), Scalar::all(0), 2, 8, 0);

	//imshow("img_display", img_display);
	//waitKey(0);

	//imshow("result", result);
	//waitKey(0);

	return maxVal;
}

double rgbTemplateMatch(string imgPath, string  tempPath)
{
	Mat img = imread(imgPath);
	Mat temp = imread(tempPath);
	Mat result;

	matchTemplate(img, temp, result, CV_TM_CCOEFF_NORMED);
	double minVal; double maxVal; Point minLoc; Point maxLoc;
	minMaxLoc(result, &minVal, &maxVal, &minLoc, &maxLoc);

	return maxVal;
}

Mat screenCapturePart(int x, int y, int w, int h) {
	/*HDC hdcSource = GetDC(NULL);
	HDC hdcMemory = CreateCompatibleDC(hdcSource);

	HBITMAP hBitmap = CreateCompatibleBitmap(hdcSource, w, h);
	HBITMAP hBitmapOld = (HBITMAP)SelectObject(hdcMemory, hBitmap);

	BitBlt(hdcMemory, 0, 0, w, h, hdcSource, x, y, SRCCOPY);
	hBitmap = (HBITMAP)SelectObject(hdcMemory, hBitmapOld);

	DeleteDC(hdcSource);
	DeleteDC(hdcMemory);*/

	int x_size = w - x, y_size = h - y; // <-- Your res for the image


	HBITMAP hBitmap; // <-- The image represented by hBitmap
	Mat matBitmap; // <-- The image represented by mat


				   // Initialize DCs
	HDC hdcSys = GetDC(NULL); // Get DC of the target capture..
	HDC hdcMem = CreateCompatibleDC(hdcSys); // Create compatible DC 



	void *ptrBitmapPixels; // <-- Pointer variable that will contain the potinter for the pixels




						   // Create hBitmap with Pointer to the pixels of the Bitmap
	BITMAPINFO bi; HDC hdc;
	ZeroMemory(&bi, sizeof(BITMAPINFO));
	bi.bmiHeader.biSize = sizeof(BITMAPINFOHEADER);
	bi.bmiHeader.biWidth = x_size;
	bi.bmiHeader.biHeight = -y_size;  //negative so (0,0) is at top left
	bi.bmiHeader.biPlanes = 1;
	bi.bmiHeader.biBitCount = 32;
	hdc = GetDC(NULL);
	hBitmap = CreateDIBSection(hdc, &bi, DIB_RGB_COLORS, &ptrBitmapPixels, NULL, 0);

	SelectObject(hdcMem, hBitmap);

	matBitmap = Mat(y_size, x_size, CV_8UC4, ptrBitmapPixels, 0);

	BitBlt(hdcMem, 0, 0, x_size, y_size, hdcSys, x, y, SRCCOPY);

	return matBitmap;
}

bool saveBitmap(LPCWSTR filename, HBITMAP bmp, HPALETTE pal)
{
	bool result = false;
	PICTDESC pd;

	pd.cbSizeofstruct = sizeof(PICTDESC);
	pd.picType = PICTYPE_BITMAP;
	pd.bmp.hbitmap = bmp;
	pd.bmp.hpal = pal;

	LPPICTURE picture;
	HRESULT res = OleCreatePictureIndirect(&pd, IID_IPicture, false,
		reinterpret_cast<void**>(&picture));

	if (!SUCCEEDED(res))
		return false;

	LPSTREAM stream;
	res = CreateStreamOnHGlobal(0, true, &stream);

	if (!SUCCEEDED(res))
	{
		picture->Release();
		return false;
	}

	LONG bytes_streamed;
	res = picture->SaveAsFile(stream, true, &bytes_streamed);

	HANDLE file = CreateFile(filename, GENERIC_WRITE, FILE_SHARE_READ, 0,
		CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL, 0);

	if (!SUCCEEDED(res) || !file)
	{
		stream->Release();
		picture->Release();
		return false;
	}

	HGLOBAL mem = 0;
	GetHGlobalFromStream(stream, &mem);
	LPVOID data = GlobalLock(mem);

	DWORD bytes_written;

	result = !!WriteFile(file, data, bytes_streamed, &bytes_written, 0);
	result &= (bytes_written == static_cast<DWORD>(bytes_streamed));

	GlobalUnlock(mem);
	CloseHandle(file);

	stream->Release();
	picture->Release();

	return result;
}


bool screenCapturePart(int x, int y, int w, int h, LPCWSTR fname) {
	HDC hdcSource = GetDC(NULL);
	HDC hdcMemory = CreateCompatibleDC(hdcSource);

	int capX = GetDeviceCaps(hdcSource, HORZRES);
	int capY = GetDeviceCaps(hdcSource, VERTRES);

	HBITMAP hBitmap = CreateCompatibleBitmap(hdcSource, w, h);
	HBITMAP hBitmapOld = (HBITMAP)SelectObject(hdcMemory, hBitmap);

	BitBlt(hdcMemory, 0, 0, w, h, hdcSource, x, y, SRCCOPY);
	hBitmap = (HBITMAP)SelectObject(hdcMemory, hBitmapOld);

	DeleteDC(hdcSource);
	DeleteDC(hdcMemory);

	HPALETTE hpal = NULL;
	if (saveBitmap(fname, hBitmap, hpal)) return true;
	return false;
}

wstring s2ws(const string& s)
{
	int len;
	int slength = (int)s.length() + 1;
	len = MultiByteToWideChar(CP_ACP, 0, s.c_str(), slength, 0, 0);
	wchar_t* buf = new wchar_t[len];
	MultiByteToWideChar(CP_ACP, 0, s.c_str(), slength, buf, len);
	wstring r(buf);
	delete[] buf;
	return r;
}

void MainBot()
{
	//These need an offset after resize for some reason
	//Offset for resize 126 : 25 

	int topLeftX = 157;
	int topLeftY = 155;
	int bottomRightX = 685;
	int bottomRightY = 685;

	//LPCWSTR name = L"TestImageOne.bmp";
	//screenCapturePart(topLeftX, topLeftY, bottomRightX, bottomRightY, name);

	char toMove;

	/*Mat blackTimer = screenCapturePart(535, 105, 600, 140);
	Mat whiteTimer = screenCapturePart(535, 670, 600, 710);
	Mat resizedBlackTimer;
	Mat resizedWhiteTimer;

	Size timerSize(27, 27);
	resize(blackTimer, resizedBlackTimer, timerSize);
	resize(whiteTimer, resizedWhiteTimer, timerSize);
	
	float returnBlack = rgbTemplateMatch(SAVE_PATH + "BlackTimer.jpg", resizedBlackTimer);
	float returnWhite = rgbTemplateMatch(SAVE_PATH + "WhiteTimer.jpg", resizedWhiteTimer);

	if (returnWhite > returnBlack)
	{
		if (returnWhite < 0.9)
		{
			toMove = 'b';
		}
		else
		{
			toMove = 'w';
		}
	}
	else if (returnBlack < returnWhite)
	{
		if (returnBlack < 0.9)
		{
			toMove = 'w';
		}
		else
		{
			toMove = 'b';
		}
	}
	else
	{
		toMove = 'w';
	}

	if (toMove == 'b' && COLOR == WHITE)
	{
		return;
	}
	if (toMove == 'w' && COLOR == BLACK)
	{
		return;
	}*/

	Mat inputImg = screenCapturePart(topLeftX, topLeftY, bottomRightX, bottomRightY);
	Mat resizedImg;

	Size size(126, 126);
	resize(inputImg, resizedImg, size);

	imshow("Title", resizedImg);
	waitKey(0);

	string FEN;
	int emptyNum = 0;
	int squareCount;
	int slashCount = 0;


	for (int row : sideArray)
	{
		for (int column : sideArray)
		{
			Rect roi;
			int resizedPieceSize = resizedImg.size().width/8;
			roi.x = resizedPieceSize * (column - 1);
			roi.y = resizedPieceSize * (row - 1);
			roi.width = resizedPieceSize;
			roi.height = resizedPieceSize;

			Mat pieceImg = resizedImg(roi);

			string filename = "D:\\Documents\\SourceTree\\ChessBot\\Screenshots\\Slices\\image" + to_string(row) + to_string(column) + ".png";
			imwrite(filename, pieceImg);

			//imshow("croppedPiece", pieceImg);
			//waitKey(0);

			/*if (squareCount % 8 == 0 && squareCount != 0 && emptyNum != 0)
			{
				FEN += to_string(emptyNum);
				emptyNum = 0;
				
				if (slashCount >= 8)
				{
					slashCount -= 8;
					FEN += "/";
				}
			}*/

			double maxVal;
			string imgPath;

			for (string templates : screenShots)
			{
				string tempPath = SAVE_PATH + "AllPieces\\" + templates + ".png";

				//imgPath = "D:\\Documents\\SourceTree\\ChessBot\\Screenshots\\AllPieces\\BRookW.png";
				
				maxVal = rgbTemplateMatch(tempPath, pieceImg);

				SetWindowText(Windows[10], to_wstring(maxVal).c_str());

				if (maxVal < 0.9)
				{
					imgPath = templates;
					continue;
				}
				else
				{
					imgPath.clear();
					break;
				}
			}

			if (maxVal < 0.8)
			{
				if (emptyNum <= 6)
				{
					slashCount++;
					emptyNum++;
					if (slashCount >= 8)
					{
						FEN += to_string(emptyNum);
						FEN += '/';
						slashCount -= 8;
						emptyNum = 0;
					}
				}
			}

			if (emptyNum != 0)
			{
				FEN += to_string(emptyNum);
				emptyNum = 0;
			}

			if (imgPath[0] == 'B')
			{
				FEN += tolower(imgPath[1]);
			}
			else
			{
				FEN += imgPath[1];
			}

			slashCount++;
			
			if (slashCount >= 8)
			{
				slashCount -= 8;
				FEN += '/';
			}
		}
		wstring wFEN = s2ws(FEN);
		SetWindowText(Windows[9], wFEN.c_str());
	}
}



// Forward declarations of functions included in this code module:
ATOM                MyRegisterClass(HINSTANCE hInstance);
BOOL                InitInstance(HINSTANCE, int);
LRESULT CALLBACK    WndProc(HWND, UINT, WPARAM, LPARAM);
INT_PTR CALLBACK    About(HWND, UINT, WPARAM, LPARAM);

int APIENTRY wWinMain(_In_ HINSTANCE hInstance,
					 _In_opt_ HINSTANCE hPrevInstance,
					 _In_ LPWSTR    lpCmdLine,
					 _In_ int       nCmdShow)
{
	UNREFERENCED_PARAMETER(hPrevInstance);
	UNREFERENCED_PARAMETER(lpCmdLine);

	// TODO: Place code here.

	// Initialize global strings
	LoadStringW(hInstance, IDS_APP_TITLE, szTitle, MAX_LOADSTRING);
	LoadStringW(hInstance, IDC_CHESSBOT, szWindowClass, MAX_LOADSTRING);
	MyRegisterClass(hInstance);

	// Perform application initialization:
	if (!InitInstance (hInstance, nCmdShow))
	{
		return FALSE;
	}

	HACCEL hAccelTable = LoadAccelerators(hInstance, MAKEINTRESOURCE(IDC_CHESSBOT));

	MSG msg;

	// Main message loop:
	while (GetMessage(&msg, nullptr, 0, 0))
	{
		if (!TranslateAccelerator(msg.hwnd, hAccelTable, &msg))
		{
			TranslateMessage(&msg);
			DispatchMessage(&msg);
		}
	}
	return (int) msg.wParam;
}

//
//  FUNCTION: MyRegisterClass()
//
//  PURPOSE: Registers the window class.
//
ATOM MyRegisterClass(HINSTANCE hInstance)
{
	WNDCLASSEXW wcex;

	wcex.cbSize = sizeof(WNDCLASSEX);

	wcex.style          = CS_HREDRAW | CS_VREDRAW;
	wcex.lpfnWndProc    = WndProc;
	wcex.cbClsExtra     = 0;
	wcex.cbWndExtra     = 0;
	wcex.hInstance      = hInstance;
	wcex.hIcon          = LoadIcon(hInstance, MAKEINTRESOURCE(IDI_CHESSBOT));
	wcex.hCursor        = LoadCursor(nullptr, IDC_ARROW);
	wcex.hbrBackground  = (HBRUSH)(COLOR_WINDOW+1);
	wcex.lpszMenuName   = MAKEINTRESOURCEW(IDC_CHESSBOT);
	wcex.lpszClassName  = szWindowClass;
	wcex.hIconSm        = LoadIcon(wcex.hInstance, MAKEINTRESOURCE(IDI_SMALL));

	return RegisterClassExW(&wcex);
}

//
//   FUNCTION: InitInstance(HINSTANCE, int)
//
//   PURPOSE: Saves instance handle and creates main window
//
//   COMMENTS:
//
//        In this function, we save the instance handle in a global variable and
//        create and display the main program window.
//

BOOL InitInstance(HINSTANCE hInstance, int nCmdShow)
{
   hInst = hInstance; // Store instance handle in our global variable

   HWND hWnd = CreateWindowW(szWindowClass, szTitle, WS_OVERLAPPEDWINDOW,
	  CW_USEDEFAULT, 0, 600, 600, nullptr, nullptr, hInstance, nullptr);

   if (!hWnd)
   {
	  return FALSE;
   }

   //SetTimer(hWnd, IDT_TEXTSECOND, 10000, (TIMERPROC)NULL);

   ShowWindow(hWnd, nCmdShow);
   UpdateWindow(hWnd);

   return TRUE;
}

//
//  FUNCTION: WndProc(HWND, UINT, WPARAM, LPARAM)
//
//  PURPOSE:  Processes messages for the main window.
//
//  WM_COMMAND  - process the application menu
//  WM_PAINT    - Paint the main window
//  WM_DESTROY  - post a quit message and return
//
//
LRESULT CALLBACK WndProc(HWND hWnd, UINT message, WPARAM wParam, LPARAM lParam)
{
	switch (message)
	{
		
	case WM_CREATE:
		{
		int buttonX = 10;
		int buttonY = 10;
		int buttonWidth = 50;
		int buttonHeight = 50;
		int radioX = buttonX;
		int radioY = buttonY + buttonHeight;
		int radioWidth = 70;
		int radioHeight = 25;


		Windows[0] = CreateWindow(
			L"BUTTON",  // Predefined class; Unicode assumed 
			L"START",      // Button text 
			WS_TABSTOP | WS_VISIBLE | WS_CHILD | BS_DEFPUSHBUTTON,  // Styles 
			buttonX,         // x position 
			buttonY,         // y position 
			buttonWidth,        // Button width
			buttonHeight,        // Button height
			hWnd,     // Parent window
			(HMENU)1,       // No menu.
			(HINSTANCE)GetWindowLong(hWnd, GWL_HINSTANCE),
			NULL);      // Pointer not needed.

		Windows[1] = CreateWindow(
			L"BUTTON",  // Predefined class; Unicode assumed 
			L"STOP",      // Button text 
			WS_TABSTOP | WS_VISIBLE | WS_CHILD | BS_DEFPUSHBUTTON,  // Styles 
			buttonX + buttonWidth,         // x position 
			buttonY,         // y position 
			buttonWidth,        // Button width
			buttonHeight,        // Button height
			hWnd,     // Parent window
			(HMENU)2,       // No menu.
			(HINSTANCE)GetWindowLong(hWnd, GWL_HINSTANCE),
			NULL);      // Pointer not needed.

		Windows[2] = CreateWindow(
			L"BUTTON",  // Predefined class; Unicode assumed 
			L"WHITE",      // Button text 
			WS_VISIBLE | WS_CHILD | BS_DEFPUSHBUTTON,  // Styles 
			radioX,         // x position 
			radioY + radioHeight,         // y position 
			radioWidth,        // Button width
			radioHeight,        // Button height
			hWnd,     // Parent window
			(HMENU)3,       // No menu.
			(HINSTANCE)GetWindowLong(hWnd, GWL_HINSTANCE),
			NULL);      // Pointer not needed.

		Windows[3] = CreateWindow(
			L"BUTTON",  // Predefined class; Unicode assumed 
			L"BLACK",      // Button text 
			WS_VISIBLE | WS_CHILD | BS_DEFPUSHBUTTON,  // Styles 
			radioX + radioWidth,         // x position 
			radioY + radioHeight,         // y position 
			radioWidth,        // Button width
			radioHeight,        // Button height
			hWnd,     // Parent window
			(HMENU)4,       // No menu.
			(HINSTANCE)GetWindowLong(hWnd, GWL_HINSTANCE),
			NULL);      // Pointer not needed.

		Windows[9] = CreateWindow(TEXT("Edit"), TEXT("FEN Here"), WS_CHILD | WS_VISIBLE | WS_BORDER, buttonX, buttonY * 25, 500, 20, hWnd, NULL, NULL, NULL);
		Windows[10] = CreateWindow(TEXT("Edit"), TEXT("Similarity Here"), WS_CHILD | WS_VISIBLE | WS_BORDER, buttonX, buttonY*20, 500, 20, hWnd, NULL, NULL, NULL);

		}

	case WM_COMMAND:
		{
			int wmId = LOWORD(wParam);
			// Parse the menu selections:
			switch (wmId)
			{
			case IDM_ABOUT:
				DialogBox(hInst, MAKEINTRESOURCE(IDD_ABOUTBOX), hWnd, About);
				break;
			case IDM_EXIT:
				DestroyWindow(hWnd);
				break;
			case 1:
				MainBot();
				RUNBOT = true;
				break;
			case 2:
				RUNBOT = false;
				break;
			case 3:
				COLOR = WHITE;
				break;
			case 4:
				COLOR = BLACK;
				break;

			default:
				return DefWindowProc(hWnd, message, wParam, lParam);
			}
		}
		break;

	case WM_PAINT:
		{
			PAINTSTRUCT ps;
			HDC hdc = BeginPaint(hWnd, &ps);
			// TODO: Add any drawing code that uses hdc here...
			EndPaint(hWnd, &ps);
		}
		break;
	case WM_DESTROY:
		PostQuitMessage(0);
		break;
	default:
		return DefWindowProc(hWnd, message, wParam, lParam);
	}
	return 0;
}

// Message handler for about box.
INT_PTR CALLBACK About(HWND hDlg, UINT message, WPARAM wParam, LPARAM lParam)
{
	UNREFERENCED_PARAMETER(lParam);
	switch (message)
	{
	case WM_INITDIALOG:
		return (INT_PTR)TRUE;

	case WM_COMMAND:
		if (LOWORD(wParam) == IDOK || LOWORD(wParam) == IDCANCEL)
		{
			EndDialog(hDlg, LOWORD(wParam));
			return (INT_PTR)TRUE;
		}
		break;
	}
	return (INT_PTR)FALSE;
}
