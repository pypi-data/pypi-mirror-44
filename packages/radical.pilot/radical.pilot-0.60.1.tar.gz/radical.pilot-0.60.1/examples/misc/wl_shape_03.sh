#!/bin/sh

. $HOME/radical/radical.synapse/ve/bin/activate

val=$1

echo $val  >   ./app_stats.dat

