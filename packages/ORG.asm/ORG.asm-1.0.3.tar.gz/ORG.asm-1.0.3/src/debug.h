/*
 * debug.h
 *
 *  Created on: 4 sept. 2012
 *      Author: coissac
 */

#ifndef DEBUG_H_
#define DEBUG_H_

#ifdef DEBUG
#undef DEBUG
#endif

#define DEBUG(format,...) fprintf(stderr,"[%s:%d] : "format"\n",__FILE__,__LINE__,__VA_ARGS__)

#include <stdint.h>

char * int2bin(int64_t i,size_t bits);


#endif /* DEBUG_H_ */
