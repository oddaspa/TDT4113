int currState = HIGH;
int prevState = HIGH;
long prev_millis;
long millis_pressed;
int buttonPin = 3;  // the pin number for input (for me a push button)
int dotPin = 13; 
int dashPin = 7;
int secPin = 5;
int current;   

void setup() {
  // initialize the button pin as a input:
  pinMode(buttonPin, INPUT);
  // initialize the dotLED(Green) as an output:
  pinMode(dotPin, OUTPUT);
  // initialize the dashLED(Red) as output:
  pinMode(dashPin, OUTPUT);
  // initialize serial communication:
  Serial.begin(9600);
  
}
void loop()
{
  prev_millis=millis(); // Counter for normal time

  // While button is pressed we count
  while(digitalRead(buttonPin) == HIGH){
    millis_pressed=millis()-prev_millis;
    digitalWrite(secPin, HIGH);
  }
  
  if(millis_pressed>50){    // Bigger than 50ms because of debounce
     if (millis_pressed>=100 && millis_pressed <=200) {
        digitalWrite(dotPin,HIGH);
        delay(300);
        // Python parse dot sign as "0".
        Serial.println("0");
        //Serial.print("Milliseconds held: ");
        //Serial.println(millis_pressed);
    }
    if(millis_pressed>200 && millis_pressed <=400){
        digitalWrite(dashPin,HIGH);
        delay(300);
        // Python parse dash as "1".
        Serial.println("1");
        //Serial.print("Milliseconds held: ");
        //Serial.println(millis_pressed);
    }
    
    millis_pressed=0;
    
  }
  digitalWrite(dotPin,LOW);
  digitalWrite(dashPin,LOW);
  digitalWrite(secPin,LOW);
}


