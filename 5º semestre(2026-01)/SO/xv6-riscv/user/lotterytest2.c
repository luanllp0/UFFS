#include "kernel/types.h"
#include "user/user.h"

#define CLASSES 4 // >= 0, <=4
#define PROCS_PER_CLASS 3
#define TOTAL_PROCS (CLASSES * PROCS_PER_CLASS)

#define STEPS 3
#define WORK_PER_STEP 64000000

void
work(int class, int id)
{
  volatile int x = 0;

  printf("C%d-P%d iniciou\n", class, id);

  for(int step = 1; step <= STEPS; step++){
    for(int i = 0; i < WORK_PER_STEP; i++){
      x++;
    }

    printf("C%d-P%d: %d/%d\n", class, id, step, STEPS);
  }

  printf("C%d-P%d terminou\n", class, id);
  exit(0);
}

int
main(void)
{
  int pid;

  for(int class = 0; class < CLASSES; class++){
    for(int id = 0; id < PROCS_PER_CLASS; id++){
      pid = fork_priority(class);

      if(pid < 0){
        printf("erro ao criar C%d-P%d\n", class, id);
        exit(1);
      }

      if(pid == 0){
        work(class, id);
      }
    }
  }

  for(int i = 0; i < TOTAL_PROCS; i++){
    wait(0);
  }

  printf("teste round robin interno finalizado\n");
  exit(0);
}
