# Risk 1:

* Scenario: When asked claude `claude 'Explain the purpose of each director'` to run against the `equity-analyzer`, the claude read all the information available in the project including design documents, architecture diagrams, DB schema.

* Why sensitive: This will share the confidential internal documents, some proprietary business logic, environment variables, security configuration. I have already decided not to put the API key as part of project .env file.

* Mitigation: Classify the data which is sensitive and make sure it is not available to claude code. Make sure there is no secrets or sensitive information as part of the source code. you can add `.claudeignore` to avoid any specific folders or files. Always review the code base for any sensitive information before proceeding to use any AI agents like claude code.

# Risk 2:

* Scenario: When asked for fundamental recommendation (zero shot)by providing the stock information. The LLM provided with a score, which doesn't have criteria how it defined that score. If used, a hallucinated value might flow through the system.

* Why sensitive: When such an unverified information is sent to external system or used directly without verification there could a financial implications.

* Mitigation: Always verify the response from LLM, make sure there is human-in-the-loop who verifies and approves to either use the parameter or send to external systems. We can also force the model to state its confidence and provide tracing capabilities for monitoring.

# Risk 3:

* Scenario: When reading web pages from on-line sources for current news, there could malicious website, which might have a content effects the prompt behaviour. This might result an unintended behaviour and LLM might respond with some bad instructions (like installing a malacious lib).

* Why sensitive: When prompt injection happens, as untrusted external content can override or manipulate the model's intended instructions. Like, we might install package which are vulnerable and might steal the data or LLM might produce lot of token which increases our billing.

* Mitigation: When reading from source like websites or any external systems, make sure the result is send to LLM with clear instruction as unverified data like <untrusted> when send to LLM. Don't allow agent to trigger any risky actions.