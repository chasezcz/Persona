# Persona

Because of the design pattern of front and back end separation used by Web applications, statistical address and function mapping is a chore.
At the same time, the designer is still interested in the compliance of the user's operation, so this program tries to realize the use of local Web application log, build user portrait to analyze user behavior.

## Data preprocessing

The purpose of this step is to get the log files sorted by 'userID' and sorted by 'date' by removing the noise and removing the interference points.
Implementation progress

- [ ] Extract the raw data as' userID '
- [ ] Extracted data sorted by 'date'
- [ ] During the extraction process, irrelevant requests and robot requests are removed

## 1.2. Sequential pattern mining

User behavior sequence mining, the intention is to find the user in a period of time to jump the operation.
The research methods are as follows

| algorithm                 | AprioriAll | GSP        | FreeSpan  | PrefixSpan |
| ------------------------- | ---------- | ---------- | --------- | ---------- |
| storage structure         | Hashtree   | Hashtree   | Hashtree  | WAP tree   |
| candidate sequences       | generated  | generated  | not       | not        |
| database segmentation     | not        | not        | yes       | yes        |
| the database scan times   | many times | many times | 3         | 2          |
| Executions                | circular   | circular   | recursive | recursive  |
| time and space efficiency | low        | low        | high      | high       |

## PrefixSpan algorithm description

Multi-dimensional portrait of users

- **User's natural attributes** : name, gender, age, email address, telephone number, occupation
- **Interest properties** : The page visited, the function used, the access path
- **Geographic information** : Reverse-check addresses via IP
- **Device properties** : Login to the desktop and use the system
- **Implied attribute**
