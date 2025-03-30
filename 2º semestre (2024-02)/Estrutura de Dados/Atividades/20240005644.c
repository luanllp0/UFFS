#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct elemStack {
    char url[61];
    struct elemStack *next;
} ElemStack;

typedef struct {
    ElemStack *top;
} Stack;

void initStack(Stack *s) {
    s->top = NULL;
}

int isEmpty(Stack *s) {
    return s->top == NULL;
}

void freeStack(Stack *s) {
    ElemStack *aux;
    while (!isEmpty(s)) {
        aux = s->top;
        s->top = s->top->next;
        free(aux);
        printf("!");
    }
}

void push(Stack *s, char link[61]) {
    ElemStack *aux = (ElemStack *)malloc(sizeof(ElemStack));
    if (aux == NULL) {
        fprintf(stderr, "Erro ao alocar memória\n");
        exit(1);
    }
    strcpy(aux->url, link);
    aux->next = s->top;
    s->top = aux;
}

void pop(Stack *s, char link[61]) {
    ElemStack *aux;
    if (isEmpty(s)) {
        return;
    }
    strcpy(link, s->top->url);
    aux = s->top;
    s->top = s->top->next;
    free(aux);
}

int main() {
    Stack stack;
    char link[61];
    char r[] = "R";
    char q[] = "Q";
    char linkout[61];

    initStack(&stack);

    while (1) {
        scanf("%60s", link); 
        int result = strcmp(link, r);
        int result2 = strcmp(link, q);

        if (result == 0) {  
            if (isEmpty(&stack)) {
                printf("empty\n");
            } else {
                pop(&stack, linkout);
                printf("%s\n", linkout);  
            }
        } else if (result2 == 0) { 
            if (isEmpty(&stack)) {
                printf("OK\n");
            } else {
                freeStack(&stack);
                printf("\n");
            }
            exit(0);
        } else {
            push(&stack, link);
        }
    }

    return 0;
}