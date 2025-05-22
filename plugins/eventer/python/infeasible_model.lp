Issue_Assignment:
MAXIMIZE
9*x_39_5_Režisér + 4*x_39_6_Režisér + 1*x_39_9_Komentátor + 9*x_40_5_Režisér + 4*x_40_6_Režisér + 1*x_40_9_Komentátor + 9*x_41_5_Režisér + 4*x_41_6_Režisér + 1*x_41_9_Komentátor + 9*x_42_5_Režisér + 4*x_42_6_Režisér + 1*x_42_9_Komentátor + 1*x_43_10_Komentátor + 5*x_43_5_Režisér + 4*x_43_9_Komentátor + 0
SUBJECT TO
ReqCount_39_Režisér: x_39_5_Režisér + x_39_6_Režisér = 1

ReqCount_39_Komentátor: x_39_9_Komentátor = 1

ReqCount_41_Režisér: x_41_5_Režisér + x_41_6_Režisér = 1

ReqCount_41_Komentátor: x_41_9_Komentátor = 1

ReqCount_42_Režisér: x_42_5_Režisér + x_42_6_Režisér = 1

ReqCount_42_Komentátor: x_42_9_Komentátor = 1

ReqCount_40_Režisér: x_40_5_Režisér + x_40_6_Režisér = 1

ReqCount_40_Komentátor: x_40_9_Komentátor = 1

ReqCount_43_Režisér: x_43_5_Režisér = 1

ReqCount_43_Komentátor: x_43_10_Komentátor + x_43_9_Komentátor = 1

NoMultiRole_39_5: x_39_5_Režisér <= 1

NoMultiRole_39_9: x_39_9_Komentátor <= 1

NoMultiRole_39_6: x_39_6_Režisér <= 1

NoMultiRole_41_5: x_41_5_Režisér <= 1

NoMultiRole_41_9: x_41_9_Komentátor <= 1

NoMultiRole_41_6: x_41_6_Režisér <= 1

NoMultiRole_42_5: x_42_5_Režisér <= 1

NoMultiRole_42_9: x_42_9_Komentátor <= 1

NoMultiRole_42_6: x_42_6_Režisér <= 1

NoMultiRole_40_5: x_40_5_Režisér <= 1

NoMultiRole_40_9: x_40_9_Komentátor <= 1

NoMultiRole_40_6: x_40_6_Režisér <= 1

NoMultiRole_43_5: x_43_5_Režisér <= 1

NoMultiRole_43_9: x_43_9_Komentátor <= 1

NoMultiRole_43_10: x_43_10_Komentátor <= 1

NoDouble_5_39_41: x_39_5_Režisér + x_41_5_Režisér <= 1

NoDouble_5_39_40: x_39_5_Režisér + x_40_5_Režisér <= 1

NoDouble_5_40_41: x_40_5_Režisér + x_41_5_Režisér <= 1

NoDouble_9_39_41: x_39_9_Komentátor + x_41_9_Komentátor <= 1

NoDouble_9_39_40: x_39_9_Komentátor + x_40_9_Komentátor <= 1

NoDouble_9_40_41: x_40_9_Komentátor + x_41_9_Komentátor <= 1

NoDouble_6_39_41: x_39_6_Režisér + x_41_6_Režisér <= 1

NoDouble_6_39_40: x_39_6_Režisér + x_40_6_Režisér <= 1

NoDouble_6_40_41: x_40_6_Režisér + x_41_6_Režisér <= 1

VARIABLES
0 <= x_39_5_Režisér <= 1 Integer
0 <= x_39_6_Režisér <= 1 Integer
0 <= x_39_9_Komentátor <= 1 Integer
0 <= x_40_5_Režisér <= 1 Integer
0 <= x_40_6_Režisér <= 1 Integer
0 <= x_40_9_Komentátor <= 1 Integer
0 <= x_41_5_Režisér <= 1 Integer
0 <= x_41_6_Režisér <= 1 Integer
0 <= x_41_9_Komentátor <= 1 Integer
0 <= x_42_5_Režisér <= 1 Integer
0 <= x_42_6_Režisér <= 1 Integer
0 <= x_42_9_Komentátor <= 1 Integer
0 <= x_43_10_Komentátor <= 1 Integer
0 <= x_43_5_Režisér <= 1 Integer
0 <= x_43_9_Komentátor <= 1 Integer
