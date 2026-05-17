#include "kernel/types.h"
#include "user/user.h"

int
main(void)
{
  int pid;

  pid = fork_priority(-1);
  if(pid == -1)
    printf("fork_priority(-1) retornou -1 corretamente\n");
  else
    printf("ERRO: fork_priority(-1) deveria retornar -1\n");

  pid = fork_priority(4);
  if(pid == -1)
    printf("fork_priority(4) retornou -1 corretamente\n");
  else
    printf("ERRO: fork_priority(4) deveria retornar -1\n");

  printf("teste de prioridade invalida finalizado\n");
  exit(0);
}
