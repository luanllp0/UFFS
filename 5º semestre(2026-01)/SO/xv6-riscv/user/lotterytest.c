#include "kernel/types.h"
#include "user/user.h"

#define STEPS 3 // qtd de passos
#define WORK_PER_STEP 100000000 // incrementos de cada passo

void
do_work(int class)
{
  // int x = 0;
  volatile int x = 0; // volatile pra evitar otimizações/remover o laço

  printf("classe %d iniciou\n", class);

  for(int step = 1; step <= STEPS; step++){ // iteração de passos
    for(int i = 0; i < WORK_PER_STEP; i++){  // iteração dos incrementos do passo
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

  for(int class = 0; class < 4; class++){ // para cada classe
    pid = fork_priority(class); // cria um processo filho da classe

    if(pid < 0){ // verificação de erro
      printf("erro ao criar processo da classe %d\n", class);
      exit(1);
    }

    if(pid == 0){ // se for o filho
      do_work(class);
    }
    // Se pid > 0, processo pai
    // O pai não entra nos ifs acima e continua o for para criar os próximos filhos
  }

  for(int i = 0; i < 4; i++){ // pai espera os processos terminar
    wait(0);
  }

  printf("teste finalizado\n");
  exit(0);
}
