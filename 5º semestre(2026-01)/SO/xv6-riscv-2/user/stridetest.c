#include "kernel/types.h"
#include "user/user.h"

#define STEPS 3
#define WORK_PER_STEP 100000000 

void
do_work(int tickets, char nome_proc)
{
  volatile int x = 0; 

  printf("Processo %c (%d bilhetes) iniciou\n", nome_proc, tickets);

  for(int step = 1; step <= STEPS; step++){ 
    for(int i = 0; i < WORK_PER_STEP; i++){  
      x++;
    }
    printf("%c: %d/%d\n", nome_proc, step, STEPS);
  }

  printf("Processo %c terminou\n", nome_proc);
  exit(0);
}

int
main(void)
{
  int pid;
  // Vetor com os bilhetes do exemplo do PDF
  int tickets_array[3] = {250, 50, 100}; 
  char nomes[3] = {'C', 'B', 'A'};

  for(int i = 0; i < 3; i++){ 
    pid = fork_tickets(tickets_array[i]); // Usa a nova syscall

    if(pid < 0){ 
      printf("erro ao criar processo %c\n", nomes[i]);
      exit(1);
    }

    if(pid == 0){ 
      do_work(tickets_array[i], nomes[i]);
    }
  }

  for(int i = 0; i < 3; i++){ 
    wait(0);
  }

  printf("Teste Stride Scheduling finalizado\n");
  exit(0);
}
