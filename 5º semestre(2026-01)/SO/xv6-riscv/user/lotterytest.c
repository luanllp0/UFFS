#include "kernel/types.h"
#include "user/user.h"

#define STEPS 3 // qtd de passos
#define WORK_PER_STEP 100000000 // incrementos de cada passo

void
do_work(int class)
{
  volatile int x = 0; // volatile pra evitar otimizações indesejadas

  printf("classe %d iniciou\n", class);

  for(int step = 1; step <= STEPS; step++){
    for(int i = 0; i < WORK_PER_STEP; i++){
      x++;
    }

    printf("C%d: %d/%d\n", class, step, STEPS);
  }

  printf("classe %d terminou\n", class);
  exit(0);
}

int
main(void)
{
  int pid;

  for(int class = 0; class < 4; class++){
    pid = fork_priority(class);

    if(pid < 0){
      printf("erro ao criar processo da classe %d\n", class);
      exit(1);
    }

    if(pid == 0){
      do_work(class);
    }
  }

  for(int i = 0; i < 4; i++){
    wait(0);
  }

  printf("teste finalizado\n");
  exit(0);
}
