Skeiron provides a Forwarding/Echo/Collect/Distribute service. \*
Forwarding - incoming message will be forwarded to configured topic. \*
Echo - incoming message will be returned to the same topic. \* Collect -
service subscribes to several topics and forwards all incoming message
to the configured topic. \* Distribute - messages from a single topic
will be published to multiple topics. \* Multiply - messages from serval
topics are forwared to multiplie topics.

.. figure:: img/Microservice%20Overview.png
   :alt: Pelops Overview

   Pelops Overview

``Skeiron`` is part of the collection of mqtt based microservices
`pelops <https://gitlab.com/pelops>`__. An overview on the microservice
architecture and examples can be found at
(http://gitlab.com/pelops/pelops).

