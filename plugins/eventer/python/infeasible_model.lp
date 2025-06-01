Issue_Assignment:
MAXIMIZE
9*x_76_5_Režisér + 4*x_76_6_Režisér + 1*x_76_9_Komentátor + 9*x_77_5_Režisér + 4*x_77_6_Režisér + 1*x_77_9_Komentátor + 1*x_78_10_Komentátor + 2*x_78_11_Režisér + 5*x_78_5_Režisér + 4*x_78_9_Komentátor + 9*x_79_5_Režisér + 4*x_79_6_Režisér + 1*x_79_9_Komentátor + 0
SUBJECT TO
ReqCount_76_Režisér: x_76_5_Režisér + x_76_6_Režisér = 1

ReqCount_76_Komentátor: x_76_9_Komentátor = 1

ReqCount_77_Režisér: x_77_5_Režisér + x_77_6_Režisér = 1

ReqCount_77_Komentátor: x_77_9_Komentátor = 1

ReqCount_78_Režisér: x_78_11_Režisér + x_78_5_Režisér = 1

ReqCount_78_Komentátor: x_78_10_Komentátor + x_78_9_Komentátor = 1

ReqCount_79_Režisér: x_79_5_Režisér + x_79_6_Režisér = 1

ReqCount_79_Komentátor: x_79_9_Komentátor = 1

NoMultiRole_76_9: x_76_9_Komentátor <= 1

NoMultiRole_76_6: x_76_6_Režisér <= 1

NoMultiRole_76_5: x_76_5_Režisér <= 1

NoMultiRole_77_9: x_77_9_Komentátor <= 1

NoMultiRole_77_6: x_77_6_Režisér <= 1

NoMultiRole_77_5: x_77_5_Režisér <= 1

NoMultiRole_78_9: x_78_9_Komentátor <= 1

NoMultiRole_78_10: x_78_10_Komentátor <= 1

NoMultiRole_78_11: x_78_11_Režisér <= 1

NoMultiRole_78_5: x_78_5_Režisér <= 1

NoMultiRole_79_9: x_79_9_Komentátor <= 1

NoMultiRole_79_6: x_79_6_Režisér <= 1

NoMultiRole_79_5: x_79_5_Režisér <= 1

NoDouble_9_76_77: x_76_9_Komentátor + x_77_9_Komentátor <= 1

NoDouble_9_76_78: x_76_9_Komentátor + x_78_9_Komentátor <= 1

NoDouble_9_77_78: x_77_9_Komentátor + x_78_9_Komentátor <= 1

NoDouble_6_76_77: x_76_6_Režisér + x_77_6_Režisér <= 1

NoDouble_6_76_78: x_76_6_Režisér <= 1

NoDouble_6_77_78: x_77_6_Režisér <= 1

NoDouble_10_76_78: x_78_10_Komentátor <= 1

NoDouble_10_77_78: x_78_10_Komentátor <= 1

NoDouble_11_76_78: x_78_11_Režisér <= 1

NoDouble_11_77_78: x_78_11_Režisér <= 1

NoDouble_5_76_77: x_76_5_Režisér + x_77_5_Režisér <= 1

NoDouble_5_76_78: x_76_5_Režisér + x_78_5_Režisér <= 1

NoDouble_5_77_78: x_77_5_Režisér + x_78_5_Režisér <= 1

VARIABLES
0 <= x_76_5_Režisér <= 1 Integer
0 <= x_76_6_Režisér <= 1 Integer
0 <= x_76_9_Komentátor <= 1 Integer
0 <= x_77_5_Režisér <= 1 Integer
0 <= x_77_6_Režisér <= 1 Integer
0 <= x_77_9_Komentátor <= 1 Integer
0 <= x_78_10_Komentátor <= 1 Integer
0 <= x_78_11_Režisér <= 1 Integer
0 <= x_78_5_Režisér <= 1 Integer
0 <= x_78_9_Komentátor <= 1 Integer
0 <= x_79_5_Režisér <= 1 Integer
0 <= x_79_6_Režisér <= 1 Integer
0 <= x_79_9_Komentátor <= 1 Integer
