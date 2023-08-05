This is a simple module to support inter process communication over stdin/stdout taking into consideration large message lengths by chunking them.

The module assume that the external communicator process also does the same chunking and unchunking with the same symbols used in this module.

# How it chunks

Messages are splitted into chunks if it is larger than a certain value also incomming messages are concated if they appeared to be in chunks

### Sending

0. new line symbol is replaced in all outgoing messages to a special symbol
1. if message is less than the threshold, the message is just preceded with a MSG tag to indicate this is an intended output message
2. if message is larger than the threshold it is splitted into chunks, first chunk is preceded with START_MSG symbol, following are preceded with the MSG symbol while the last chunk is preceeded with the END_MSG symbol


### Receiving
1. if message started with MSG symbol and no previous START_MSG symbol received before then this line is considered as the full message stripping symbols from the beginning
2. if a start message is received then this line is saved and concated with all the following lines that have the MSG symbol until the END_MSG symbol is received. All symbols are stripped and lines are concated to create the final msg
3. final message has its new line symbol replaced with the actual "\n" character
