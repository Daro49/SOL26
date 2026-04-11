class Main : Object{
    run [| 
        x := self attr: 3.
        y := [| ret := (self attr) greaterThan: 0. ] whileTrue:
            [| r := ((self attr) asString) print.
            r := self attr: ((self attr) minus: 1).].

        _ := (y asString) print.
    ]
}