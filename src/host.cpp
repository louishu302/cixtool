#include "host.h"
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <time.h>


host::host()
{
   int i;
   const int seed_size = 4096;
   data_ware = (uint32_t*)malloc(sizeof(uint32_t)*1024);

   srand((unsigned)time(NULL));
   for (i = 0; i < seed_size/4; i++)
        data_ware[i] = rand();

}

host::~host()
{
    if (data_ware)
        delete data_ware;
    
}

int host::spi_rd(uint64_t address, uint32_t *data_out)
{
    uint32_t  start_data;
    start_data = address%4096; 
    *data_out = data_ware[start_data];
    printf("received address: 0x%lX, send out data: 0x%X\n",address,*data_out);

    return 0;
}
