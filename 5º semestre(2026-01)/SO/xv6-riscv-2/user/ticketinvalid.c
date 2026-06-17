#include "kernel/types.h"
#include "user/user.h"

int
main(void)
{
  int pid;

  // Teste 1: Zero bilhetes (causaria divisão por zero: 10000 / 0)
  pid = fork_tickets(0); 
  if(pid == -1)
    printf("fork_tickets(0) bloqueado corretamente (retornou -1)\n");
  else
    printf("ERRO: fork_tickets(0) falhou na protecao\n");

  // Teste 2: Bilhetes negativos
  pid = fork_tickets(-50); 
  if(pid == -1)
    printf("fork_tickets(-50) bloqueado corretamente (retornou -1)\n");
  else
    printf("ERRO: fork_tickets(-50) falhou na protecao\n");

  // Teste 3: Bilhetes acima da constante (Ex: > 10000)
  pid = fork_tickets(15000); 
  if(pid == -1)
    printf("fork_tickets(15000) bloqueado corretamente (retornou -1)\n");
  else
    printf("ERRO: fork_tickets(15000) falhou na protecao\n");

  printf("Teste de seguranca de bilhetes finalizado\n");
  exit(0);
}
