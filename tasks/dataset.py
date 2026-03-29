QUESTION_BANK = {
    "python_basics": [
        {
            "question": "Explain the difference between a list and a tuple in Python. When would you use each?",
            "topic": "python_basics",
            "difficulty": "easy",
            "expected_keywords": ["mutable", "immutable", "list", "tuple", "performance", "hashable"],
            "expected_score_strong": 9,
            "expected_score_average": 6,
            "expected_score_weak": 3,
        },
        {
            "question": "What are Python decorators and how do they work internally?",
            "topic": "python_basics",
            "difficulty": "medium",
            "expected_keywords": ["wrapper", "function", "closure", "args", "kwargs", "higher-order"],
            "expected_score_strong": 9,
            "expected_score_average": 5,
            "expected_score_weak": 2,
        },
    ],
    "data_structures": [
        {
            "question": "Explain how a hash map works. What happens during a collision?",
            "topic": "data_structures",
            "difficulty": "medium",
            "expected_keywords": ["hash", "bucket", "collision", "chaining", "open addressing", "load factor"],
            "expected_score_strong": 9,
            "expected_score_average": 6,
            "expected_score_weak": 2,
        },
        {
            "question": "Compare arrays and linked lists in terms of time complexity for common operations.",
            "topic": "data_structures",
            "difficulty": "easy",
            "expected_keywords": ["O(1)", "O(n)", "access", "insertion", "deletion", "contiguous", "pointer"],
            "expected_score_strong": 9,
            "expected_score_average": 6,
            "expected_score_weak": 3,
        },
    ],
    "algorithms": [
        {
            "question": "Explain the difference between BFS and DFS. When would you prefer one over the other?",
            "topic": "algorithms",
            "difficulty": "medium",
            "expected_keywords": ["breadth", "depth", "queue", "stack", "shortest path", "traversal", "graph"],
            "expected_score_strong": 9,
            "expected_score_average": 6,
            "expected_score_weak": 2,
        },
        {
            "question": "What is dynamic programming? Explain with an example.",
            "topic": "algorithms",
            "difficulty": "hard",
            "expected_keywords": ["subproblem", "memoization", "tabulation", "optimal", "overlapping", "fibonacci"],
            "expected_score_strong": 9,
            "expected_score_average": 5,
            "expected_score_weak": 2,
        },
    ],
    "system_design": [
        {
            "question": "How would you design a URL shortener like bit.ly?",
            "topic": "system_design",
            "difficulty": "hard",
            "expected_keywords": ["hash", "database", "redirect", "base62", "collision", "cache", "scalability"],
            "expected_score_strong": 9,
            "expected_score_average": 5,
            "expected_score_weak": 2,
        },
        {
            "question": "Explain the CAP theorem and its implications for distributed systems.",
            "topic": "system_design",
            "difficulty": "hard",
            "expected_keywords": ["consistency", "availability", "partition tolerance", "trade-off", "distributed"],
            "expected_score_strong": 9,
            "expected_score_average": 5,
            "expected_score_weak": 1,
        },
    ],
    "oop_concepts": [
        {
            "question": "Explain the SOLID principles with examples.",
            "topic": "oop_concepts",
            "difficulty": "medium",
            "expected_keywords": ["single responsibility", "open closed", "liskov", "interface segregation", "dependency inversion"],
            "expected_score_strong": 9,
            "expected_score_average": 5,
            "expected_score_weak": 2,
        },
        {
            "question": "What is polymorphism? Explain the difference between compile-time and runtime polymorphism.",
            "topic": "oop_concepts",
            "difficulty": "easy",
            "expected_keywords": ["overloading", "overriding", "inheritance", "virtual", "dynamic dispatch"],
            "expected_score_strong": 9,
            "expected_score_average": 6,
            "expected_score_weak": 3,
        },
    ],
    "databases": [
        {
            "question": "Explain the difference between SQL and NoSQL databases. When would you choose one over the other?",
            "topic": "databases",
            "difficulty": "medium",
            "expected_keywords": ["relational", "schema", "ACID", "scalability", "document", "key-value", "flexible"],
            "expected_score_strong": 9,
            "expected_score_average": 6,
            "expected_score_weak": 2,
        },
        {
            "question": "What is database indexing and how does a B-tree index work?",
            "topic": "databases",
            "difficulty": "hard",
            "expected_keywords": ["index", "B-tree", "balanced", "leaf", "lookup", "O(log n)", "pages"],
            "expected_score_strong": 9,
            "expected_score_average": 5,
            "expected_score_weak": 1,
        },
    ],
}

CANDIDATE_ANSWERS = {
    "python_basics_0": {
        "strong": {
            "answer_text": "Lists are mutable sequences in Python, meaning you can modify them after creation by adding, removing, or changing elements. Tuples are immutable, so once created, their elements cannot be changed. This immutability makes tuples hashable, so they can be used as dictionary keys or set elements. Tuples also have a slight performance advantage due to their fixed size - Python can optimize memory allocation. I use lists when I need a collection that will change over time, like accumulating results. I use tuples for fixed collections like database records, function return values with multiple elements, or when I want to signal that the data should not be modified.",
            "quality_score": 9,
            "keywords_present": ["mutable", "immutable", "hashable", "performance", "list", "tuple"],
            "reasoning_quality": "excellent",
        },
        "average": {
            "answer_text": "Lists can be changed after you create them but tuples cannot be changed. Lists use square brackets and tuples use parentheses. I usually use lists when I need to add or remove items and tuples when the data stays the same. Lists are more commonly used in general.",
            "quality_score": 6,
            "keywords_present": ["mutable", "list", "tuple"],
            "reasoning_quality": "partial",
        },
        "weak": {
            "answer_text": "Lists and tuples are both used to store data. Lists use brackets and tuples use parentheses. I think tuples are faster but I am not sure why. I mostly just use lists for everything.",
            "quality_score": 3,
            "keywords_present": ["list", "tuple"],
            "reasoning_quality": "poor",
        },
    },
    "python_basics_1": {
        "strong": {
            "answer_text": "Decorators are higher-order functions that take a function as input and return a new function that usually extends or modifies the behavior of the original. Internally, when you use the @decorator syntax, Python passes the decorated function as an argument to the decorator function. The decorator typically defines a wrapper function using *args and **kwargs to accept any arguments, calls the original function inside, and returns the result possibly with modifications. This is possible because of closures - the wrapper function retains access to the original function through the enclosing scope. Common use cases include logging, authentication checks, caching with functools.lru_cache, and timing functions.",
            "quality_score": 9,
            "keywords_present": ["wrapper", "function", "closure", "args", "kwargs", "higher-order"],
            "reasoning_quality": "excellent",
        },
        "average": {
            "answer_text": "Decorators are functions that modify other functions. You put @decorator_name above a function definition and it changes what the function does. They use a wrapper function inside. I have used them for things like login_required in web frameworks.",
            "quality_score": 5,
            "keywords_present": ["wrapper", "function"],
            "reasoning_quality": "partial",
        },
        "weak": {
            "answer_text": "Decorators are the @ symbol you put before functions. They do something to the function but I am not exactly sure how they work internally. I have seen them in Flask for routes.",
            "quality_score": 2,
            "keywords_present": ["function"],
            "reasoning_quality": "poor",
        },
    },
    "data_structures_0": {
        "strong": {
            "answer_text": "A hash map stores key-value pairs using a hash function that converts keys into array indices. The hash function takes a key, computes an integer hash code, and maps it to a bucket index using modulo with the array size. Collisions occur when two different keys map to the same index. There are two main strategies: chaining, where each bucket holds a linked list of entries, and open addressing, where we probe for the next available slot using linear probing, quadratic probing, or double hashing. The load factor (number of entries divided by number of buckets) determines when to resize the array. Typically when the load factor exceeds 0.75, the array is doubled and all entries are rehashed. Average case operations are O(1) but worst case is O(n) when all keys collide.",
            "quality_score": 9,
            "keywords_present": ["hash", "bucket", "collision", "chaining", "open addressing", "load factor"],
            "reasoning_quality": "excellent",
        },
        "average": {
            "answer_text": "A hash map uses a hash function to map keys to positions in an array. When two keys get the same position it is called a collision. You can handle collisions by chaining which uses linked lists at each position. Hash maps give O(1) average time for lookups.",
            "quality_score": 6,
            "keywords_present": ["hash", "collision", "chaining", "bucket"],
            "reasoning_quality": "partial",
        },
        "weak": {
            "answer_text": "A hash map stores keys and values. It uses some kind of function to find where to put things. I think collisions are when two things go to the same spot. I am not sure how they fix that.",
            "quality_score": 2,
            "keywords_present": ["hash", "collision"],
            "reasoning_quality": "poor",
        },
    },
    "data_structures_1": {
        "strong": {
            "answer_text": "Arrays store elements in contiguous memory locations, providing O(1) random access by index but O(n) for insertion and deletion in the middle since elements must be shifted. Linked lists store elements as nodes with pointers to the next node, giving O(1) insertion and deletion when you have a reference to the position but O(n) for access since you must traverse from the head. Arrays have better cache locality due to contiguous memory, making them faster in practice for iteration. Dynamic arrays amortize resizing to O(1) append. Linked lists use more memory per element due to pointer storage. I would choose arrays for random access patterns and linked lists for frequent insertions and deletions at known positions.",
            "quality_score": 9,
            "keywords_present": ["O(1)", "O(n)", "access", "insertion", "deletion", "contiguous", "pointer"],
            "reasoning_quality": "excellent",
        },
        "average": {
            "answer_text": "Arrays let you access elements by index in O(1) time but inserting in the middle is O(n). Linked lists are better for insertion since you just change pointers but accessing an element is O(n) since you have to go through the list. Arrays use contiguous memory.",
            "quality_score": 6,
            "keywords_present": ["O(1)", "O(n)", "access", "insertion", "contiguous", "pointer"],
            "reasoning_quality": "partial",
        },
        "weak": {
            "answer_text": "Arrays store things next to each other in memory and linked lists use pointers. Arrays are faster for finding things and linked lists are better for adding things. I am not sure about the exact time complexity.",
            "quality_score": 3,
            "keywords_present": ["contiguous", "pointer"],
            "reasoning_quality": "poor",
        },
    },
    "algorithms_0": {
        "strong": {
            "answer_text": "BFS explores nodes level by level using a queue data structure, visiting all neighbors of a node before moving to the next level. DFS explores as deep as possible along each branch before backtracking, using a stack or recursion. BFS guarantees finding the shortest path in unweighted graphs because it explores nodes in order of their distance from the source. DFS is better for problems requiring exploration of all paths like maze solving, topological sorting, or detecting cycles. BFS uses more memory O(w) where w is the maximum width of the tree, while DFS uses O(h) where h is the height. I prefer BFS for shortest path problems and level-order processing, and DFS for problems involving connectivity, backtracking, or when memory is a concern in deep narrow graphs.",
            "quality_score": 9,
            "keywords_present": ["breadth", "depth", "queue", "stack", "shortest path", "traversal", "graph"],
            "reasoning_quality": "excellent",
        },
        "average": {
            "answer_text": "BFS uses a queue and explores level by level while DFS uses a stack and goes deep first. BFS is better for finding shortest paths. DFS is better for things like checking if a path exists. Both can traverse all nodes in a graph.",
            "quality_score": 6,
            "keywords_present": ["breadth", "depth", "queue", "stack", "shortest path", "graph"],
            "reasoning_quality": "partial",
        },
        "weak": {
            "answer_text": "BFS goes wide and DFS goes deep. I think BFS uses a queue. They are both used for searching through graphs or trees. I usually just use whichever one I remember.",
            "quality_score": 2,
            "keywords_present": ["queue", "graph"],
            "reasoning_quality": "poor",
        },
    },
    "algorithms_1": {
        "strong": {
            "answer_text": "Dynamic programming is an optimization technique that solves complex problems by breaking them into smaller overlapping subproblems and storing their solutions to avoid redundant computation. There are two approaches: top-down with memoization, where you use recursion with a cache, and bottom-up with tabulation, where you fill a table iteratively from the base cases up. For example, computing Fibonacci numbers naively has O(2^n) time complexity due to repeated calculations. With DP, you store each F(i) once, reducing it to O(n) time and O(n) space, or O(1) space if you only keep the last two values. The key conditions for DP applicability are optimal substructure (optimal solution contains optimal solutions to subproblems) and overlapping subproblems.",
            "quality_score": 9,
            "keywords_present": ["subproblem", "memoization", "tabulation", "optimal", "overlapping", "fibonacci"],
            "reasoning_quality": "excellent",
        },
        "average": {
            "answer_text": "Dynamic programming breaks problems into smaller subproblems and remembers the answers so you do not solve them again. Like with Fibonacci, instead of recalculating the same values you store them. There is memoization which is top down and tabulation which is bottom up.",
            "quality_score": 5,
            "keywords_present": ["subproblem", "memoization", "tabulation", "fibonacci"],
            "reasoning_quality": "partial",
        },
        "weak": {
            "answer_text": "Dynamic programming is when you save results so you do not have to calculate them again. I know Fibonacci is a common example. It makes things faster but I am not sure when exactly to use it.",
            "quality_score": 2,
            "keywords_present": ["fibonacci"],
            "reasoning_quality": "poor",
        },
    },
    "system_design_0": {
        "strong": {
            "answer_text": "For a URL shortener, I would use a service that takes a long URL and generates a unique short code using base62 encoding of an auto-incremented ID or a hash of the URL truncated to 7 characters. The mapping is stored in a database with the short code as the primary key. When a user visits the short URL, the service looks up the code, retrieves the original URL, and sends a 301 or 302 redirect. For scalability, I would add a distributed cache like Redis in front of the database for frequent lookups. To handle collisions in the hash approach, I would append characters or regenerate. For high availability, I would use database replication and multiple application servers behind a load balancer. Analytics can be added by logging each redirect with timestamp and user agent.",
            "quality_score": 9,
            "keywords_present": ["hash", "database", "redirect", "base62", "collision", "cache", "scalability"],
            "reasoning_quality": "excellent",
        },
        "average": {
            "answer_text": "I would create a database table with the short code and the original URL. When someone submits a URL, I generate a short code and store it. When someone visits the short URL, I look up the code and redirect them. I would use a hash function to generate the codes.",
            "quality_score": 5,
            "keywords_present": ["hash", "database", "redirect"],
            "reasoning_quality": "partial",
        },
        "weak": {
            "answer_text": "I would store the URLs in a database and give each one a short code. When someone clicks the short link it goes to the real URL. I am not sure how to handle lots of users at once.",
            "quality_score": 2,
            "keywords_present": ["database"],
            "reasoning_quality": "poor",
        },
    },
    "system_design_1": {
        "strong": {
            "answer_text": "The CAP theorem states that a distributed system can guarantee at most two of three properties simultaneously: Consistency (all nodes see the same data at the same time), Availability (every request receives a response), and Partition Tolerance (the system continues to function despite network partitions). Since network partitions are inevitable in distributed systems, the real choice is between CP and AP systems. CP systems like HBase or MongoDB with strong consistency sacrifice availability during partitions. AP systems like Cassandra or DynamoDB prioritize availability and use eventual consistency. The choice depends on the application: banking needs strong consistency (CP) while social media feeds can tolerate eventual consistency (AP) for better user experience.",
            "quality_score": 9,
            "keywords_present": ["consistency", "availability", "partition tolerance", "trade-off", "distributed"],
            "reasoning_quality": "excellent",
        },
        "average": {
            "answer_text": "CAP theorem says you can only have two out of consistency, availability, and partition tolerance in a distributed system. Consistency means all nodes have the same data. Availability means the system always responds. Partition tolerance means it works even if the network splits.",
            "quality_score": 5,
            "keywords_present": ["consistency", "availability", "partition tolerance", "distributed"],
            "reasoning_quality": "partial",
        },
        "weak": {
            "answer_text": "I have heard of CAP theorem. It is about choosing between consistency and availability I think. Something about distributed systems not being able to have everything at once.",
            "quality_score": 1,
            "keywords_present": ["consistency", "availability"],
            "reasoning_quality": "poor",
        },
    },
    "oop_concepts_0": {
        "strong": {
            "answer_text": "SOLID is five principles for maintainable object-oriented design. Single Responsibility: a class should have only one reason to change, like separating data access from business logic. Open/Closed: classes should be open for extension but closed for modification, achieved through inheritance and interfaces. Liskov Substitution: subtypes must be substitutable for their base types without altering program correctness, meaning a Square should not violate invariants of Rectangle if it inherits from it. Interface Segregation: clients should not depend on interfaces they do not use, so split large interfaces into specific ones. Dependency Inversion: high-level modules should depend on abstractions not concrete implementations, using dependency injection to decouple components.",
            "quality_score": 9,
            "keywords_present": ["single responsibility", "open closed", "liskov", "interface segregation", "dependency inversion"],
            "reasoning_quality": "excellent",
        },
        "average": {
            "answer_text": "SOLID stands for five principles. Single Responsibility means a class does one thing. Open Closed means you can extend but not modify. Liskov is about substituting child classes for parents. Interface Segregation means smaller interfaces. Dependency Inversion means depending on abstractions.",
            "quality_score": 5,
            "keywords_present": ["single responsibility", "open closed", "liskov", "interface segregation", "dependency inversion"],
            "reasoning_quality": "partial",
        },
        "weak": {
            "answer_text": "SOLID is some principles for OOP. I remember Single Responsibility means classes should do one thing. I think Open Closed is about not changing existing code. I do not remember the other three very well.",
            "quality_score": 2,
            "keywords_present": ["single responsibility", "open closed"],
            "reasoning_quality": "poor",
        },
    },
    "oop_concepts_1": {
        "strong": {
            "answer_text": "Polymorphism means the ability of objects of different types to be treated through a common interface. Compile-time polymorphism is resolved at compile time through method overloading, where multiple methods have the same name but different parameter signatures. Runtime polymorphism is resolved at runtime through method overriding, where a subclass provides a specific implementation of a method defined in its parent class. In languages like Java and C++, runtime polymorphism uses virtual method tables for dynamic dispatch. The actual method called depends on the runtime type of the object, not the reference type. This enables writing flexible code that works with base class references while invoking specialized behavior.",
            "quality_score": 9,
            "keywords_present": ["overloading", "overriding", "inheritance", "virtual", "dynamic dispatch"],
            "reasoning_quality": "excellent",
        },
        "average": {
            "answer_text": "Polymorphism means one interface can have multiple implementations. Compile-time polymorphism is method overloading where you have methods with the same name but different parameters. Runtime polymorphism is method overriding where a child class redefines a parent method. It uses inheritance.",
            "quality_score": 6,
            "keywords_present": ["overloading", "overriding", "inheritance"],
            "reasoning_quality": "partial",
        },
        "weak": {
            "answer_text": "Polymorphism means many forms. I think it is when different objects can do the same thing differently. Like a dog and cat both make sounds but different sounds. I am not sure about the compile time and runtime difference.",
            "quality_score": 3,
            "keywords_present": ["inheritance"],
            "reasoning_quality": "poor",
        },
    },
    "databases_0": {
        "strong": {
            "answer_text": "SQL databases are relational, storing data in tables with predefined schemas and using SQL for queries. They provide ACID guarantees (Atomicity, Consistency, Isolation, Durability) making them ideal for transactional workloads like banking. NoSQL databases encompass document stores like MongoDB, key-value stores like Redis, column-family stores like Cassandra, and graph databases like Neo4j. They offer flexible schemas and horizontal scalability. I choose SQL when data relationships are complex and consistency is critical, when the schema is well-defined, or when complex joins and aggregations are needed. I choose NoSQL for rapidly evolving schemas, massive scale with simple access patterns, or when the data model naturally fits a non-relational structure like social graphs or real-time analytics.",
            "quality_score": 9,
            "keywords_present": ["relational", "schema", "ACID", "scalability", "document", "key-value", "flexible"],
            "reasoning_quality": "excellent",
        },
        "average": {
            "answer_text": "SQL databases use tables and are relational with a fixed schema. NoSQL databases are more flexible and can store data as documents or key-value pairs. SQL is good when you need ACID transactions and NoSQL is better for scalability. MongoDB is a popular NoSQL database.",
            "quality_score": 6,
            "keywords_present": ["relational", "schema", "ACID", "scalability", "flexible"],
            "reasoning_quality": "partial",
        },
        "weak": {
            "answer_text": "SQL uses tables and NoSQL does not. SQL is older and more structured. NoSQL is newer and more flexible. I usually use SQL because I am more familiar with it.",
            "quality_score": 2,
            "keywords_present": ["flexible"],
            "reasoning_quality": "poor",
        },
    },
    "databases_1": {
        "strong": {
            "answer_text": "Database indexing creates a separate data structure that maintains a sorted reference to rows, enabling faster lookups without scanning the entire table. A B-tree index is a self-balancing tree where each node can have multiple children. Internal nodes store keys that guide the search, and leaf nodes contain pointers to actual data rows. The tree stays balanced by splitting and merging nodes during insertions and deletions, guaranteeing O(log n) lookup time. Each node corresponds to a disk page, minimizing I/O operations. B-trees are optimal for range queries since leaf nodes are often linked. The trade-off is slower writes since the index must be updated, and additional storage space. Choosing what to index involves analyzing query patterns and considering the selectivity of columns.",
            "quality_score": 9,
            "keywords_present": ["index", "B-tree", "balanced", "leaf", "lookup", "O(log n)", "pages"],
            "reasoning_quality": "excellent",
        },
        "average": {
            "answer_text": "Indexing makes database queries faster by creating a structure that points to the data. A B-tree index is a balanced tree where lookups take O(log n) time. The leaf nodes point to the actual rows in the table. Indexes slow down writes because they need to be updated.",
            "quality_score": 5,
            "keywords_present": ["index", "B-tree", "balanced", "leaf", "O(log n)"],
            "reasoning_quality": "partial",
        },
        "weak": {
            "answer_text": "Indexing makes queries faster. I know B-tree is a type of index but I am not sure how it works exactly. You add indexes to columns that you search on a lot.",
            "quality_score": 1,
            "keywords_present": ["index", "B-tree"],
            "reasoning_quality": "poor",
        },
    },
}

TOPIC_LIST = list(QUESTION_BANK.keys())


def get_question_for_round(task_id: str, round_number: int) -> dict:
    task_question_map = {
        "easy": [("python_basics", 0)],
        "medium": [("data_structures", 0), ("algorithms", 0)],
        "hard": [
            ("python_basics", 1),
            ("data_structures", 0),
            ("system_design", 0),
            ("databases", 1),
        ],
    }
    sequence = task_question_map.get(task_id, task_question_map["easy"])
    idx = min(round_number - 1, len(sequence) - 1)
    topic, q_idx = sequence[idx]
    return QUESTION_BANK[topic][q_idx]


def get_candidate_answer(topic: str, question_index: int, strength_level: str) -> dict:
    key = f"{topic}_{question_index}"
    answers = CANDIDATE_ANSWERS.get(key, {})
    return answers.get(strength_level, {
        "answer_text": "I am not sure about this topic.",
        "quality_score": 1,
        "keywords_present": [],
        "reasoning_quality": "poor",
    })


def get_question_index_in_topic(question_text: str) -> tuple:
    for topic, questions in QUESTION_BANK.items():
        for idx, q in enumerate(questions):
            if q["question"] == question_text:
                return topic, idx
    return "python_basics", 0
