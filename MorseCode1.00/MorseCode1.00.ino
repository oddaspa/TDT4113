int currState = HIGH;
int prevState = HIGH;
long prev_millis;
long millis_pressed;
int buttonPin = 3;  // the pin number for input (for me a push button)
int dotPin = 13; 
int dashPin = 7;
int secPin = 5;
int current;   
long pauseTime=0;
long buttonRelease=0;


const float T = 200; // T is in ms. Change to prefered amount.
const float dotTime = T;  
const float dashTime = 3*T;
const float letterPauseTime = 3*T;
const float wordPauseTime = 7*T;

const int dotSignal = 1; // Given by assignment.
const int dashSignal = 2;
const int letterPauseSignal = 3;
const int wordPauseSignal = 4;

void setup() {
  // initialize the button pin as a input:
  pinMode(buttonPin, INPUT);
  // initialize the dotLED(Green) as an output:
  pinMode(dotPin, OUTPUT);
  // initialize the dashLED(Red) as output:
  pinMode(dashPin, OUTPUT);
  // initialize the secLED(Blue) as output:
  pinMode(secPin, OUTPUT);
  // initialize serial communication:
  Serial.begin(9600);
  
}
void loop()
{
  prev_millis=millis(); // Counter for normal time
  
  // While button is pressed we count
  while(digitalRead(buttonPin) == HIGH){
    digitalWrite(secPin, HIGH);
    if (pauseTime != 0){
      getPause(pauseTime); // Method implemented below
      pauseTime=0;
    }
    millis_pressed=millis()-prev_millis;
    buttonRelease=millis();

  }
  
  pauseTime=millis()-buttonRelease; // Time button is not pressed
  if(millis_pressed>50){    // Bigger than 50ms because of debounce
    if(millis_pressed>dotTime+100){
      digitalWrite(dashPin,HIGH);
      delay(300);
      // Python parse dash as "1".
      Serial.print(dashSignal);
      //Serial.print("Milliseconds held: ");
      //Serial.println(millis_pressed);
    }
    else{
      digitalWrite(dotPin,HIGH);
      delay(300);
      // Python parse dot sign as "0".
      Serial.print(dotSignal);
      //Serial.print("Milliseconds held: ");
      //Serial.println(millis_pressed);
    }

    
    millis_pressed=0;
    
  }
  
  digitalWrite(dotPin,LOW);
  digitalWrite(dashPin,LOW);
  digitalWrite(secPin,LOW);
}
void getPause(long pauseTime){
    if(pauseTime>letterPauseTime && pauseTime<letterPauseTime+400){
      Serial.print(letterPauseSignal);
    }
    if(pauseTime>wordPauseTime+400){
      Serial.print(wordPauseSignal);
    }
    // Make else method for resetting the process
}


