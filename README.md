# rollercoaster
Implement rollercoaster model on Edison

TODO
Spawn multiple cars to advanvce in parallel using threads.
Get the messages to represent closely what actions and states do.



Capabilities

<b>TURNSTILE</b></br>
<p>A turnstile has only a single capability. It will allow a passenger through to the platform (CONTROL). If the platform is full, the CONTROL will send a message back indicating that to be the case. If there is room for the passenger, the CONTROL will send a message accepting the passenger.</p>
<ul>
  <li>Sample message: [2017-10-17 11:15:12.423] 10.11.2.123 TURNSTILE requests entry for passenger #3</li>
</ul>

<b>CONTROL</b></br>
<p>The platform is represented by the CONTROL. This control will wait for passengers until the platform is full. Once the platform is full, the CONTROL will refuse any additional passengers. CONTROL will broadcast a pickup message when there are enough passengers. The CONTROL will only reply to the first available car that responds to the pickup request.</p>
<ul>
  <li>Sample message: [2017-10-17 11:15:13.312] 10.11.2.123 CONTROL allow passenger #3
  <li>Sample message: [2017-10-17 11:15:13.312] 10.11.2.123 CONTROL platform is full
  <li>Sample message: [2017-10-17 11:16:48.765] 10.11.2.123 CONTROL pickup [Passenger #1, Passenger #2, Passenger #3]
</ul>

CAR

<b>MONITOR</b></br>
<p>The monitor process does not send or respond to any message. The monitor simply logs all messages it sees on the subscribed topic into a file for analysis.</p>
