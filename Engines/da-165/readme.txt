General hints:

DisasterArea-1.65pc  is the popcount-version
DisasterArea-1.65    is a little bit slower and should run on most actual cpus
DisasterArea-1.65old should run on any cpu 

pawn_value = 256
ply = 16

Engine-Options:
Hash: size in MB (max 16 GB)  
Threads: max 4 cores
MultiPV: limited to max 64 variants 
GUI_Lag: time in millisec for gui-delay
Timing:  remaining time is divided with this value basically (but will be changed by other criteria)
PawnStruct: just this, set it to 0, and DesasterArea will ignore doublepawns etc.
Candidates: pawns, that could become a passer
Passers: against stronger engine always wrong (to high or to low ;-) )
Mobility: mobility of pieces (no pawns and king)
King_Safety: mainly pawn_shield and some extras
King_Attacks: just this
CenterControl: knights, king and pawns are excluded
Pins: pieces pinned to king
Hanging: pieces under attack
PSQT: = pst 
Oracle: some general rules (same as misc in Stockfish), no precalc of psqt
AB_Window: value 0 turns it off (no fail-high or low)
QVS_Checks: allowed depth in quiesce for silent check-moves
Check_Extension: 1 ply
Single_Move_Extension: engine is in check and there is only one move
SE_Extension: singular move extension, triggers in at remaining depth >= 8 ply)
Min_Split_Depth: for 2 cores (5 ply default seems best)
Min_SE_Depth: default 8 ply 
Min_LMR_Depth: remaining depth to do LMR-Reductions, set it to 1600, and LMR is switched off
Max_Static_Nullcut_Depth: 0 means no static_nullcut (can be usefull for analysis)
Max_Razoring_Depth: 0  means no razoring (can be usefull for analysis)
Max_NC_Futility_Depth: 0 means no nodecount futility, moves that will be completly ignored
Max_SEE_Futility_Depth: 0 means no see futility, only good captures
Max_Gain_Futility_Depth: 0 means no positionell gain futility
Ponder: dummy, pondering is controlled by gui
Eval_Hash: testing feature, memory is allocated always
Pawn_Hash: testing feature, memory is allocated always
Nullmove: can be switched off here
Null_Verification: dito
Delta_Pruning: only captures, that raise value to or above alpha in quiesce
Singular_Extensions: redundand, can be switched off also by setting Min_SE_Depth to 1600
Clear_hash: inits main, eval and pawn hash

Console:
you can use the perft command after entering a position: perft depth

Other:
you can use an ini-file to overwrite the default-values. That may be usefull for tools like cutechess-cli.
The example ini-file must be renamed to da.ini to become active and contains the "Cognac-Stettings" 
by Brendan J. Norman.          