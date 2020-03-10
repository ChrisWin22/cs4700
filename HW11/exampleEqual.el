(def listp (a) 
    (not (atom a)))
(set x 1)
(set q (quote (x 2)))
(set p (quote (1 4)))
# # tests that two nested lists are the same structure with the same contents
(def equal (a b)
    (if (eq a b) 
        True 
        (if (or (not (listp a)) 
                (not (listp b))) 
            False 
            (and (equal (first a) (first b)) 
                  (equal (rest a) (rest b))))))
(equal q p)