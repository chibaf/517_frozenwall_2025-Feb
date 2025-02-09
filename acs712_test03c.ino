//CAS712
//使う電流センサのアンペア数
float Ampere = 5;
//現在の電流値(mA)．
float current;
//オフセット値(V)．デフォだと0Vの時センサ値は512(レンジを5Vにすると2.5V)なので ．
float offset = 2.505;
//レンジ調整値．0Vに調整した後，電源等でこの電流計の値が合っているかをチェックして，ズレていれば調整する．
float range = 0.95;
//forを回す回数．大きくすると処理が遅くなるが，電流値は安定する．10000times/secがanalogReadの限界な事に注意．
int times = 100;

void setup() {
  Serial.begin(9600);
  analogReadResolution(14); 
}

void loop() {
  current = 0;
  for(int i = 0; i < times; i++){
    //1.5~3.5Vレンジなので2.5Vオフセットすると-1~1V．これを-5~5Vにする為5をかけている．
    current += ((float)(analogRead(A0)) / 1023 * Ampere - offset) / range * 5 * 1000 / (float)(times);
  }
  //Serial.print("Current(mA) = ");
  Serial.println(current,4);
}
