#ifndef HOST_H_
#define HOST_H_


#include <stdio.h>
#include <stdint.h>

    class host {
        public:
            host();
            ~host();

            // int spi_rd(uint64_t address, uint32_t bytecount, uint32_t *data_out);
            int spi_rd(uint64_t address, uint32_t *data_out);
        private:
            uint32_t     *data_ware;

    };


#endif     //end host_h