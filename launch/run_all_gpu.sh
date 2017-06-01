sets=(1 2 3 Round1Test)

for set in sets
do
	for bf in ~/udacity_competition/Didi-Release-2/Data/$set/*.bag
	do
		bf_name="${filename%.*}"
		gnome-terminal --tab --title="$set_$bf_name" -e "bash -c \"./kojaks_launch.sh $set $bf_name 60 -x -t; bash\""
	done
done