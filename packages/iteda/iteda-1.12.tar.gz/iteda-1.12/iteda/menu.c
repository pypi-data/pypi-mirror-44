//Calibration/LedManager$ cat configDAC_2.c 
#include <stdio.h>      // standard input / output functions
#include <stdlib.h>
#include <string.h>     // string function definitions
#include <unistd.h>     // UNIX standard function definitions
#include <fcntl.h>      // File control definitions
#include <errno.h>      // Error number definitions
#include <termios.h>    // POSIX terminal control definitions
#include <endian.h>


#define	MAX_REGS	14

//unsigned char LE8toBE (unsigned char littleEndian);

int main (int argc,char** argv)
{
	struct termios tty;
	unsigned char data[4];
	int USB, i, n_written;
	int value[4];
	int trigger[4];
	unsigned int led_time[8];
	
	
	
	if(argc != MAX_REGS+1)
	{
		printf("Faltan parametros\nPor favor verificar  4 x { [TON] [T_DELAY] [Power_VALUE(mV)] } + [Trigger int/ext] + [Trigger_select]\n\n");
		return 0;
	}
	
	for(i = 0; i < 4; i++)
	{
		value[i] = atoi(argv[3+(i*3)]);

		if (value[i] < 0 || value[i] > 4096)
		{
			printf("El valor ingresado para los DACs debe estar entre 0mV y 208mV\n");
			return 0;
		}
	}

	for(i = 0; i < 2; i++)
	{
		trigger[i] = atoi(argv[13+i]);
		
		if (trigger[i] < 0 || trigger[i] > 9)
		{
			printf("El valor ingresado para los Trigger_value es incorrecto\n");
			return 0;
		}
	}
	
	for(i = 0; i < 4; i++)
	{
		led_time[i] = atoi(argv[1+(i*3)]);
		
		if (led_time[i] < 0 || led_time[i] > 65535)
		{
			printf("El valor ingresado para los TOFFs es incorrecto\n");
			return 0;
		}
	}
	
	for(i = 0; i < 4; i++)
	{
		led_time[i+4] = atoi(argv[2+(i*3)]);
		
		if (led_time[i+4] < 0 || led_time[i+4] > 65535)
		{
			printf("El valor ingresado para los TONs es incorrecto\n");
			return 0;
		}
	}
	
	/* Open File Descriptor */
	USB = open( "/dev/ttyUSB0", O_RDWR| O_NONBLOCK | O_NDELAY );

	/* Error Handling */
	if ( USB < 0 )
	{
	    printf("Error al abrir /dev/ttyUSB0 \n");
	}

	/* *** Configure Port *** */
	memset (&tty, 0, sizeof tty);

	/* Error Handling */
	if ( tcgetattr ( USB, &tty ) != 0 )
	{
	    printf("Error al configurar ttyUSB0 \n");
	}

	/* Set Baud Rate */
	cfsetospeed (&tty, B19200);
	cfsetispeed (&tty, B19200);

	/* Setting other Port Stuff */
	tty.c_cflag     &=  ~PARENB;        // Make 8n1
	tty.c_cflag     &=  ~CSTOPB;
	tty.c_cflag     &=  ~CSIZE;
	tty.c_cflag     |=  CS8;
	tty.c_cflag     &=  ~CRTSCTS;       // no flow control
	tty.c_lflag     =   0;          // no signaling chars, no echo, no canonical processing
	tty.c_oflag     =   0;                  // no remapping, no delays
	tty.c_cc[VMIN]      =   0;                  // read doesn't block
	tty.c_cc[VTIME]     =   5;                  // 0.5 seconds read timeout

	tty.c_cflag     |=  CREAD | CLOCAL;     // turn on READ & ignore ctrl lines
	tty.c_iflag     &=  ~(IXON | IXOFF | IXANY);// turn off s/w flow ctrl
	tty.c_lflag     &=  ~(ICANON | ECHO | ECHOE | ISIG); // make raw
	tty.c_oflag     &=  ~OPOST;              // make raw

	/* Flush Port, then applies attributes */
	tcflush( USB, TCIFLUSH );

	if ( tcsetattr ( USB, TCSANOW, &tty ) != 0)
	{
	    printf("Error \n");
	}

	
	
	/* *** WRITE TIME_ON AND DELAY*** */
	for(i = 0; i < 8; i++)
	{
	
		data[2] = (unsigned char)(led_time[i] & 0x00FF);
		usleep(100);
	        n_written = write( USB, & data[2], sizeof(char));
		tcdrain(USB);
	}

	/* *** WRITE trigger_value and int/ext*** */
	for(i = 0; i < 2; i++)
	{

		data[2] = (unsigned char)(trigger[i] & 0x00FF);
		usleep(100);
		n_written = write( USB, & data[2], sizeof(char));
		tcdrain(USB);

	}

	/* *** WRITE DACS*** */
	for(i = 0; i < 4; i++)
	{

		data[2] = (unsigned char)(value[i] & 0x00FF);
		usleep(100);
		n_written = write( USB, & data[2], sizeof(char));
		tcdrain(USB);

	}


	close(USB);	
	printf("Flawless victory\n");
	return 0;

}