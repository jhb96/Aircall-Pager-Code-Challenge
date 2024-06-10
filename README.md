## Aircall Technical CODE CHALLENGE - Aircall Pager

### [INSTRUCTIONS](CHALLENGE.md)

### PROPOSED SOLUTION

In the development of the Aircall Pager system, I had the option to employ an event-driven architecture, which is well-suited for systems where asynchrony and real-time handling of events are crucial. 
However, I decided to adopt an architecture more aligned with ***Domain-Driven Design (DDD) principles***, emphasizing the importance of a model-centric approach that focuses on complex business logic and behavior. Besides, can be extended seamlessly to include a REST API interface where each endpoint can be mapped to a specific service handled method from pager_service.py (e.g. /alerts, /escalation_policies, /services, etc).


#### DDD-Inspired Service-Oriented Architecture

The architecture I selected draws heavily from DDD principles, integrating patterns that reinforce the importance of the domain model and ensuring that the business logic remains the focal point of our development:

- Rich Domain Model: By creating a detailed domain model, we encapsulate and closely align the software model with the business domain. This is evident in our implementation of various domain entities and value objects, such as Alert, EscalationPolicy, and MonitoredService

- Repository: We used the Repository Pattern to provide a collection-like interface for accessing domain objects, which abstracts away the details of data access and storage. This helps in managing domain objects without needing to know how they are persisted.

- Services: Critical business actions are handled by domain services (pager_service.py), which orchestrate complex operations involving multiple domain entities. This ensures that business rules are correctly applied and that the domain logic is not diluted.

- Layered Architecture: We maintain a clear separation between the domain model, application logic, and infrastructure, which supports the scalability and manageability of the system.



#### Implementation Details
I have implemented the system in Python, trying to avoid use non-native libraries such as pydantic for the modeling or pytest for testing.


##### Domain Model
Core Functionality: The service layer, particularly through domain services like pager_service.py, encapsulates the business logic of the system. This layer is responsible for handling complex business operations such as alert processing, notification dispatch based on escalation policies, and managing timeouts.

##### Service Locator Pattern

The pager_service.py utilizes the the service_provider to fetch the required services such as IMailService, I etc with This approach simplifies the management of these dependencies and centralizes their configuration.


##### Database guarantees

The MonitoredServiceRepository serves as the abstraction layer between the domain logic and the database operations related to MonitoredService entities.
Persistence Guarantees: Once a transaction involving a MonitoredService has been committed, it is permanently stored in the database. This durability ensures 
that the service status remains consistent even in the event of a system failure.


##### Testing
Each test case is structured to simulate the actions, inputs, and subsequent reactions defined in the use case. This might involve simulating system events (like receiving an alert or a health check), and verifying the output against expected outcomes.
Since I have only defined interfaces for the adapters but no real implementations, I have created simple mocks of those classes to run the code and check the model is modified as expected.
By running these tests, we can ensure that the system behaves as expected and that the business logic is correctly implemented.


### Running

To run the tests, simply execute the following command:

```bash
make test
```
or
```bash
python -m unittest discover -v -s ./tests -p "test_*.py"
```


To start a local server, run the following command.
First, install the dependencies by running the following command (only for server)

```bash
make install
```
or
```bash
pip install -r requirements.txt
```


```bash
make start-server
```
or 
```bash
python -m uvicorn server:app --reload
```




### Next Steps

- Implement the REST API interface to expose the functionality of the Pager system. This would involve creating endpoints for managing alerts, escalation policies, and services, as well as handling notifications and health checks.

- Implement the concrete implementations of the service interfaces (IMailService, ISMSService, etc.) to enable the system to send notifications via email, SMS, and other channels.

- Implement the database layer to persist the domain entity MonitoredService and ensure data consistency and durability.


### Improvements

- Implement a more robust error handling mechanism to handle exceptions and edge cases more effectively.

- Implement a more comprehensive testing suite that covers a wider range of scenarios and edge cases.

