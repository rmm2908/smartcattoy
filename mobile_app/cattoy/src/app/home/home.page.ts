import { Component } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { CapacitorHttp } from '@capacitor/core';
import { webSocket, WebSocketSubject } from 'rxjs/webSocket';


@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss'],
})
export class HomePage {
  myWebSocket: WebSocketSubject<any> = webSocket('wss://hackathoncattoy.azurewebsites.net');

  constructor(private httpClient: HttpClient) {
    this.myWebSocket.asObservable().subscribe(data => console.log(data));
    /*this.myWebSocket.subscribe(    
      msg => console.log('message received: ' + msg), 
      // Called whenever there is a message from the server    
      err => console.log(err), 
      // Called if WebSocket API signals some kind of error    
      () => console.log('complete') 
      // Called when connection is closed (for whatever reason)  
   );*/
  }

  moveForward() {
    console.log("Forward Clicked");
    this.myWebSocket.next({"motor1PW": 60, "motor1D": 0, "motor2PW": 60, "motor2D": 0});
    //this.sendRequestToServer("{\"motor1PW\": 60, \"motor1D\": 0, \"motor2PW\": 60, \"motor2D\": 0}");
  };

  moveBackward() {
    console.log("Backward Clicked");
    this.myWebSocket.next({"motor1PW": 60, "motor1D": 1, "motor2PW": 60, "motor2D": 1});
    //this.sendRequestToServer("{\"motor1PW\": 60, \"motor1D\": 1, \"motor2PW\": 60, \"motor2D\": 1}");
  };

  moveLeft() {
    console.log("Left Clicked");
    this.myWebSocket.next({"motor1PW": 60, "motor1D": 0, "motor2PW": 60, "motor2D": 1});
    //this.sendRequestToServer("{\"motor1PW\": 60, \"motor1D\": 0, \"motor2PW\": 60, \"motor2D\": 1}");
  };

  moveRight() {
    console.log("Right Clicked");
    this.myWebSocket.next({"motor1PW": 60, "motor1D": 1, "motor2PW": 60, "motor2D": 0});
    //this.sendRequestToServer("{\"motor1PW\": 60, \"motor1D\": 1, \"motor2PW\": 60, \"motor2D\": 0}");
  };

  sendRequestToServer(command: String) {
    /*const httpOptions = {
      headers: new HttpHeaders({
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'POST',
          'Access-Control-Allow-Headers': 'Content-Type, Authorization',
          'Content-Type': 'application/json; charset=utf-8'
      })
  };
  
    this.httpClient.post("https://192.168.50.225:9988", command, httpOptions).subscribe(response => {
      console.log("Request Response: ", response);
    });*/
    const options = {
      url: 'http://192.168.50.225:9988',
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        'Content-Type': 'application/json; charset=utf-8'
      },
      data: command,
    };

    CapacitorHttp.post(options).then(response => {
      console.log(response)
    });
  }
}
