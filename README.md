To run the venv use:

`python3 -m venv venv`

`source venv/bin/activate`

To run the game:

`python3 main.py`


Nota: Ao criar o ficheiro para gerar o tabuleiro, não separar os elementos da matriz por virgula, apenas por espaços


# Resultados do Benchmarking - Lights Out Solver

A tabela abaixo apresenta a comparação de performance entre os algoritmos implementados, variando o tamanho do tabuleiro ($N \times N$). Todos os testes foram realizados com tabuleiros gerados a partir de 10 movimentos aleatórios (Dificuldade Média).

| Algoritmo | Tamanho | Tempo (s) | Movimentos | Memória (Máx) | Estados Analisados |
| :--- | :---: | :--- | :---: | :--- | :--- |
| **BFS** | 3 | 0.0000 | 2 | 9 | 2 |
| **BFS** | 4 | 0.1000 | 6 | 1949 | 2179 |
| **BFS** | 5 | 0.0810 | 4 | 6511 | 975 |
| **BFS** | 6 | N/D | N/D | N/D | N/D |
| **DFS** | 3 | 0.0120 | 2 | 348 | 504 |
| **DFS** | 4 | 0.1560 | 74 | 3220 | 3318 |
| **DFS** | 5 | N/D | N/D | N/D | N/D |
| **DFS** | 6 | N/D | N/D | N/D | N/D |
| **IDS** | 3 | 0.0000 | 2 | 2 | 21 |
| **IDS** | 4 | 3.0330 | 6 | 6 | 930712 |
| **IDS** | 5 | 0.1640 | 4 | 4 | 49728 |
| **IDS** | 6 | N/D | N/D | N/D | N/D |
| **UCS** | 3 | 0.0000 | 2 | 57 | 18 |
| **UCS** | 4 | 0.1840 | 6 | 1949 | 3690 |
| **UCS** | 5 | 0.6710 | 4 | 33188 | 7486 |
| **UCS** | 6 | N/D | N/D | N/D | N/D |
| **Greedy - Lights On Count** | 3 | 2.7670 | 2 | 16 | 3 |
| **Greedy - Lights On Count** | 4 | 0.6840 | 8 | 169 | 13 |
| **Greedy - Lights On Count** | 5 | 1.3540 | 12 | 776 | 37 |
| **Greedy - Lights On Count** | 6 | 0.6510 | 12 | 1190 | 36 |
| **Greedy - Parity** | 3 | 0.6000 | 2 | 16 | 3 |
| **Greedy - Parity** | 4 | 0.8040 | 6 | 566 | 45 |
| **Greedy - Parity** | 5 | 0.7260 | 10 | 1327 | 62 |
| **Greedy - Parity** | 6 | 1.0790 | 56 | 23290 | 737 |
| **Greedy - Isolated Lights*** | 3 | 1.1830 | 2 | 16 | 3 |
| **Greedy - Isolated Lights*** | 4 | 0.8350 | 6 | 155 | 12 |
| **Greedy - Isolated Lights*** | 5 | 0.7510 | 4 | 94 | 5 |
| **Greedy - Isolated Lights*** | 6 | 0.6050 | 8 | 342 | 11 |
| **Astar - Lights On Count** | 3 | 8.2840 | 2 | 16 | 3 |
| **Astar - Lights On Count** | 4 | 0.7560 | 6 | 934 | 104 |
| **Astar - Lights On Count** | 5 | 0.8170 | 4 | 136 | 7 |
| **Astar - Lights On Count** | 6 | 0.6380 | 8 | 1840 | 60 |
| **Wheighted Astar - Lights On Count** | 3 | 2.1000 | 2 | 16 | 3 |
| **Wheighted Astar - Lights On Count** | 4 | 0.7330 | 6 | 162 | 14 |
| **Wheighted Astar - Lights On Count** | 5 | 0.9210 | 4 | 756 | 37 |
| **Wheighted Astar - Lights On Count** | 6 | 1.1440 | 10 | 1530 | 49 |
| **Astar - Parity** | 3 | 0.7000 | 2 | 16 | 3 |
| **Astar - Parity** | 4 | 0.6750 | 6 | 1942 | 383 |
| **Astar - Parity** | 5 | 0.7690 | 4 | 323 | 16 |
| **Astar - Parity** | 6 | 1.4090 | 8 | 72288 | 3051 |
| **Wheighted Astar - Parity** | 3 | 0.9160 | 2 | 16 | 3 |
| **Wheighted Astar - Parity** | 4 | 0.5430 | 6 | 1082 | 117 |
| **Wheighted Astar - Parity** | 5 | 0.4740 | 6 | 686 | 34 |
| **Wheighted Astar - Parity** | 6 | 0.6180 | 8 | 1995 | 70 |
| **Astar - Isolated Lights** | 3 | 2.4670 | 2 | 16 | 3 |
| **Astar - Isolated Lights** | 4 | 0.8450 | 6 | 868 | 99 |
| **Astar - Isolated Lights** | 5 | 0.6510 | 4 | 92 | 5 |
| **Astar - Isolated Lights** | 6 | 0.9280 | 8 | 3843 | 134 |
| **Wheighted Astar - Isolated Lights** | 3 | 0.8670 | 2 | 16 | 3 |
| **Wheighted Astar - Isolated Lights** | 4 | 1.0020 | 6 | 231 | 20 |
| **Wheighted Astar - Isolated Lights** | 5 | 9.1850 | 4 | 92 | 5 |
| **Wheighted Astar - Isolated Lights** | 6 | 0.9410 | 8 | 521 | 17 |


**Notas sobre as métricas:**
* **Tempo (s):** Tempo total de execução do solver em segundos.
* **Movimentos:** Número de cliques na solução encontrada (Qualidade da Solução).
* **Memória:** Tamanho máximo atingido pela estrutura de dados de suporte (Fila/Pilha/Heap).
* **Estados:** Número total de configurações de tabuleiro analisadas durante a procura.