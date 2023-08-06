This package is a collection of various programming patterns, adapted from Android code. They are useless by themselves - only by extending and completing them can they be useful to you. Good luck!

Contained within:


    Constants interface (application.constants_interface)

    Defaulting Dictionary (patterns.defaulting_dict)

    Enumeration (enumeration)

        Matchers (enumeration.matcher.abstract_matcher)

        Value matcher (enumeration.matcher.abstract_value_matcher)

        Representables (enumeration.enums.abstract_representable)

        Visitor Pattern (enumeration.visitor.abstract_visitor)

    Event Handling Pattern (eventhandling)

        Event Distributors

        Event Monitors (eventhandling.eventmonitoring.event_monitor)

        Event Trackers (eventhandling.abstract_event_tracker)

        Events (eventhandling.event)

        Reactions (eventhandling.abstract_reaction)

    Executable Pattern (patterns.executable)

        Do-Nothing Executables (patterns.do_nothing_executable)

    Factory Pattern (factories)

        Custom Factories (factories.abstract_custom_factory)

    Listener Pattern (listeners)

        Dummy Listeners (listeners.dummy_listener)

        Listener Registry (listeners.abstract_listener_registry)

        Proxy Listeners (listeners.proxy_listener)

        Subject Listeners (abstract_event_subject_listener)

        No-Subject Listener (abstract_event_subject_unused_listener)

    Matcher Pattern (enumeration.matcher.abstract_value_matcher)

    Registry Pattern (application.abstract_registry)

        Context Based Registry Locator (application.base_context_registry_locator)

    Rules and Rule Engine Patterns (rules)

        Logging Rules (rules.logging_rule_engine)

        Stateful Rules (rules.abstract_stateful_rule)

        Rule Engines (rules.rule_engine)

        Basic Rules (rules.abstract_rule)

    Quicksort (sorting.abstract_quick_sorter)

    Transformer Pattern (transforming)

        Populator Pattern (transforming.abstract_populator)


Just extend the pattern you're looking to use, fill in the mandatory items, and there you go!