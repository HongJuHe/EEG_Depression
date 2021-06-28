#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>
#include "thinkgear.h"
#include <fcntl.h>

/**
 * Prompts and waits for the user to press ENTER.
 */
void wait() {
	printf("\n");
	printf("===== 뇌파 측정 종료 =====\n");
	fflush(stdout);
	getc(stdin);
}

/**
 * Program which prints ThinkGear Raw Wave Values to stdout.
 */
int __cdecl main(int argc, char** argv) {
	if (argc > 1) {
		GetEEG(argv[1]);
	}
	else {
		GetEEG(60);
	}
}

int GetEEG(int t) {
	char* comPortName = NULL;
	int   dllVersion = 0;
	int   connectionId = 0;
	int   packetsRead = 0;
	int   errCode = 0;

	double secondsToRun = 0;
	time_t startTime = 0;
	time_t currTime = 0;
	char currTimeStr[256] = { 0, };
	//char  *currTimeStr  = NULL;//
	int set_filter_flag = 0;
	int count = 0;
	/*new file dir*/
	FILE* fp = NULL;
	errno_t err;

	// D:/ThinkGearData/data.txt
	err = fopen_s(&fp, "D:/ThinkGearData/data0.txt", "w");

	/* Print driver version number */
	dllVersion = TG_GetVersion();
	printf("Stream SDK for PC version: %d\n", dllVersion);

	/* Get a connection ID handle to ThinkGear */
	connectionId = TG_GetNewConnectionId();
	if (connectionId < 0) {
		fprintf(stderr, "ERROR: TG_GetNewConnectionId() returned %d.\n",
			connectionId);
		wait();
		exit(EXIT_FAILURE);
	}

	/* Set/open stream (raw bytes) log file for connection */
	errCode = TG_SetStreamLog(connectionId, "streamLog.txt");
	if (errCode < 0) {
		fprintf(stderr, "ERROR: TG_SetStreamLog() returned %d.\n", errCode);
		wait();
		exit(EXIT_FAILURE);
	}

	/* Set/open data (ThinkGear values) log file for connection */
	errCode = TG_SetDataLog(connectionId, "dataLog.txt");
	if (errCode < 0) {
		fprintf(stderr, "ERROR: TG_SetDataLog() returned %d.\n", errCode);
		wait();
		exit(EXIT_FAILURE);
	}

	/* Attempt to connect the connection ID handle to serial port "COM5" */
	/* NOTE: On Windows, COM10 and higher must be preceded by \\.\, as in
	 *       "\\\\.\\COM12" (must escape backslashes in strings).  COM9
	 *       and lower do not require the \\.\, but are allowed to include
	 *       them.  On Mac OS X, COM ports are named like
	 *       "/dev/tty.MindSet-DevB-1".
	 */
	comPortName = "\\\\.\\COM5";
	errCode = TG_Connect(connectionId,
		comPortName,
		TG_BAUD_57600,
		TG_STREAM_PACKETS);
	if (errCode < 0) {
		fprintf(stderr, "ERROR: TG_Connect() returned %d.\n", errCode);
		wait();
		exit(EXIT_FAILURE);
	}

	/* Keep reading ThinkGear Packets from the connection for 5 seconds... */
	secondsToRun = t;
	// secondsToRun = 60; // 측정 시간, 초 단위
	startTime = time(NULL);
	while (difftime(time(NULL), startTime) < secondsToRun) {

		/* Read all currently available Packets, one at a time... */
		do {
			/* Read a single Packet from the connection */
			packetsRead = TG_ReadPackets(connectionId, 1);

			/* If TG_ReadPackets() was able to read a Packet of data... */
			if (packetsRead == 1) {

				/* If the Packet containted a new raw wave value... */
				if (TG_GetValueStatus(connectionId, TG_DATA_RAW) != 0) {

					/* Get the current time as a string */
					//currTime = time( NULL );
					time_t now_time;
					time(&now_time);
					ctime_s(currTimeStr, sizeof(currTimeStr), &now_time);

					//currTimeStr = ctime_s(&char[256], sizeof(char[256]), &currTime);

					/* Get and print out the new raw value */
					fprintf(stdout, ": data raw: %d\n",
						(int)TG_GetValue(connectionId, TG_DATA_RAW)); // 저장 중 cmd에 출력되는 부분

					// [ rawValue * (1.8/4096) ] / 2000
					// double voltage = ((float)TG_GetValue(connectionId, TG_DATA_RAW) * (1.8 / 4096)) / 2000; //
					// fprintf(stdout, ": 데이터 voltage value: %f\n", voltage);

					//fprintf( stdout, "%s: raw: %d\n", currTimeStr,
					//       (int)TG_GetValue(connectionId, TG_DATA_RAW) );
					/* new!! */
					fprintf(fp, "%d ",
						(int)TG_GetValue(connectionId, TG_DATA_RAW));
					fflush(stdout);
					// 저장 형식? 숫자 뒤 띄어쓰기

				} /* end "If Packet contained a raw wave value..." */

			} /* end "If TG_ReadPackets() was able to read a Packet..." */

		} while (packetsRead > 0); /* Keep looping until all Packets read */

	} /* end "Keep reading ThinkGear Packets for 5 seconds..." */

	printf("auto read test begin:\n");
	fflush(stdin);

	errCode = TG_EnableAutoRead(connectionId, 1);
	if (errCode == 0) {
		packetsRead = 0;
		errCode = MWM15_setFilterType(connectionId, MWM15_FILTER_TYPE_50HZ);//MWM15_FILTER_TYPE_60HZ
		printf("MWM15_setFilterType: %d\n", errCode);
		while (packetsRead < 3000) {
			/* If raw value has been updated ... */
			if (TG_GetValueStatus(connectionId, TG_DATA_RAW) != 0) {

				/* Get and print out the updated raw value */
				//printf( "%d ",
				//        (int)TG_GetValue(connectionId, TG_DATA_RAW) );
				//fflush( stdout );
				if (packetsRead % 5 == 0) { // too much stdout operation will lose some data
					printf(" %d ",
						(int)TG_GetValue(connectionId, TG_DATA_RAW)); // 저장 다 끝나고 뭉쳐서 나오는 부분
				}
				else {
					TG_GetValue(connectionId, TG_DATA_RAW);
				}
				packetsRead++;

				//wait for a while to call MWM15_getFilterType
				if (packetsRead == 800 || packetsRead == 1600) {// at lease 1s after MWM15_setFilterType cmd
					set_filter_flag++;
					errCode = MWM15_getFilterType(connectionId);

					printf(" \nMWM15_getFilterType   result: %d  index: %d\n", errCode, packetsRead);
				}
			}

			if (TG_GetValueStatus(connectionId, MWM15_DATA_FILTER_TYPE) != 0) {

				/* Get and print out the updated raw value */
				printf("\n#### @@@ Find Filter type: %d  set_filter_flag: %d  index: %d\n",
					(int)TG_GetValue(connectionId, MWM15_DATA_FILTER_TYPE), set_filter_flag, packetsRead);
				break;
			}
		}

		errCode = TG_EnableAutoRead(connectionId, 0); //stop
		printf("auto read test stoped: %d \n", errCode);
	}
	else {
		printf("auto read test failed: %d \n", errCode);
	}

	TG_Disconnect(connectionId); // disconnect test

	/* Clean up */
	TG_FreeConnection(connectionId);

	/* End program */
	wait();
	return(EXIT_SUCCESS);
}
