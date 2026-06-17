#include "kernel/types.h"
#include "user/user.h"

#define PROCS_TOTAL 3
#define TICKETS_PADRAO 100 
#define PASSADAS_DESEJADAS 3

void
work(int id)
{
  int meu_pid = getpid(); 
  printf("P%d (PID %d) iniciou.\n", id, meu_pid);

  for(int step = 1; step <= PASSADAS_DESEJADAS; step++){ 
    
    // O 'volatile' obriga o compilador a executar o laço de verdade
    for(volatile int i = 0; i < 20000000; i++){
    }
    
  }

  printf("P%d (PID %d) terminou.\n", id, meu_pid);
  exit(0);
}

int
main(void)
{
  int pid;

  printf("Iniciando Teste de empates:\n");

  for(int id = 1; id <= PROCS_TOTAL; id++){ 
    pid = fork_tickets(TICKETS_PADRAO); 

    if(pid < 0){ 
      printf("erro ao criar P%d\n", id);
      exit(1);
    }

    if(pid == 0){ 
      work(id);
    }
  }

  for(int i = 0; i < PROCS_TOTAL; i++){ 
    wait(0);
  }

  printf("\nTeste finalizado!\n");
  exit(0);
}
