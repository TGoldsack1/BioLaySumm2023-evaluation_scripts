#

mkdir ./models
mkdir ./models/bartscore

curl -c ./cookie -s -L "https://drive.google.com/uc?export=download&id=1lq3eYl-kWZTZt5yfmECkdBA5MQn4i2_F" > /dev/null
curl -Lb ./cookie "https://drive.google.com/uc?export=download&confirm=`awk '/download/ {print $NF}' ./cookie`&id=1lq3eYl-kWZTZt5yfmECkdBA5MQn4i2_F" -o ./models/bartscore/st1_plos.zip
unzip ./models/bartscore/st1_plos.zip -d ./models/bartscore/st1_plos

curl -c ./cookie -s -L "https://drive.google.com/uc?export=download&id=1vP7TuG_QgfXf5cOKmz15qvfKd8G6AH06" > /dev/null
curl -Lb ./cookie "https://drive.google.com/uc?export=download&confirm=`awk '/download/ {print $NF}' ./cookie`&id=1vP7TuG_QgfXf5cOKmz15qvfKd8G6AH06" -o ./models/bartscore/st1_elife.zip
unzip ./models/bartscore/st1_elife.zip -d ./models/bartscore/st1_elife

curl -c ./cookie -s -L "https://drive.google.com/uc?export=download&id=1za45oJZN-I8avSyeaQOwBXtjaUNYGA4B" > /dev/null
curl -Lb ./cookie "https://drive.google.com/uc?export=download&confirm=`awk '/download/ {print $NF}' ./cookie`&id=1za45oJZN-I8avSyeaQOwBXtjaUNYGA4B" -o ./models/bartscore/st2_abstract.zip
unzip ./models/bartscore/st2_abstract.zip -d ./models/bartscore/st2_abstract

curl -c ./cookie -s -L "https://drive.google.com/uc?export=download&id=1_triNenBHvPoyT_XfDANEumIeHxYg1V8" > /dev/null
curl -Lb ./cookie "https://drive.google.com/uc?export=download&confirm=`awk '/download/ {print $NF}' ./cookie`&id=1_triNenBHvPoyT_XfDANEumIeHxYg1V8" -o ./models/bartscore/st2_laysumm.zip
unzip ./models/bartscore/st2_laysumm.zip -d ./models/bartscore/st2_laysumm