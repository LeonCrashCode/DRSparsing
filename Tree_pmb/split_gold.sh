
cat gold/p[0-9]1/*/sentence.tree.enhanced2 > tst.tree

cat gold/p[0-9]0/*/sentence.tree.enhanced2 > dev.tree

cat gold/p[0-9][2-9]/*/sentence.tree.enhanced2 > gold.tree

python tree2oracle_tcn.py gold.tree
python get_dict_tcn.py gold.tree.oracle.out > gold.dict
