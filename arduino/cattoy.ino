int ena = 5;
int in1 = 6;
int in2 = 7;

int enb = 10;
int in3 = 11;
int in4 = 12;
char payload[64];
String input = "EMPTY";

void setup() {
  Serial.begin(9600); 

  pinMode(ena, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);

  pinMode(enb, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);
  }

void forward() {
    digitalWrite(in1, HIGH);
    digitalWrite(in2, LOW);
    analogWrite(ena, 255);

    digitalWrite(in3, HIGH);
    digitalWrite(in4, LOW);
    analogWrite(enb, 255);
}

void backward() {
    digitalWrite(in1, LOW);
    digitalWrite(in2, HIGH);
    analogWrite(ena, 255);

    digitalWrite(in3, LOW);
    digitalWrite(in4, HIGH);
    analogWrite(enb, 255);
}

void left() {
    digitalWrite(in1, LOW);
    digitalWrite(in2, LOW);
    analogWrite(ena, 255);

    digitalWrite(in3, HIGH);
    digitalWrite(in4, LOW);
    analogWrite(enb, 255);
}

void right() {
    digitalWrite(in1, HIGH);
    digitalWrite(in2, LOW);
    analogWrite(ena, 255);

    digitalWrite(in3, LOW);
    digitalWrite(in4, LOW);
    analogWrite(enb, 255);
}

void stopMoving() {
    digitalWrite(in1, LOW);
    digitalWrite(in2, LOW);     

    digitalWrite(in3, LOW);
    digitalWrite(in4, LOW);     
}

void loop() {
  if (Serial.available() > 0) {
    input = Serial.readStringUntil( '\n' );
    if(input.equals("forward")) {
      forward();
    }
    if(input.equals("backward")) {
      backward();
    }
    if(input.equals("left")) {
      left();
    }
    if(input.equals("right")) {
      right();
    }
    if(input.equals("stop")) {
      stopMoving();
    }
  }
}
