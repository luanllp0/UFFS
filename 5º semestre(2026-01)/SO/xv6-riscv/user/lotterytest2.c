#include "kernel/types.h"
#include "user/user.h"

#define CLASSES 4 // >= 0, <=4
#define PROCS_PER_CLASS 3
#define TOTAL_PROCS (CLASSES * PROCS_PER_CLASS)

#define STEPS 3 // qtd de passos
#define WORK_PER_STEP 64000000 // incrementos de cada passo

void
work(int class, int id)
{
  volatile int x = 0; // volatile pra evitar otimizações/remover o laço

  printf("C%d-P%d iniciou\n", class, id);

  for(int step = 1; step <= STEPS; step++){ // iteração de passos
    for(int i = 0; i < WORK_PER_STEP; i++){ // iteração dos incrementos do passo
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

  for(int class = 0; class < CLASSES; class++){ // para cada classe
    for(int id = 0; id < PROCS_PER_CLASS; id++){ // para cada processo definido para a classe
      pid = fork_priority(class); // cria um processo filho

      if(pid < 0){ // verificação de erro
        printf("erro ao criar C%d-P%d\n", class, id);
        exit(1);
      }

      if(pid == 0){ // se for o filho
        work(class, id);
      }
      // Se pid > 0, processo pai
      // O pai não entra nos ifs acima e continua o for para criar os próximos filhos
    }
  }

  for(int i = 0; i < TOTAL_PROCS; i++){ // pai espera os processos terminar
    wait(0);
  }

  printf("teste round robin interno finalizado\n");
  exit(0);
}
