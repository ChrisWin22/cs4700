(set y 3)
            
(def fact (x) 
    (if (eq x 1) 
        x 
        (* x (fact (- x 1)))))

(+ (fact y) y)