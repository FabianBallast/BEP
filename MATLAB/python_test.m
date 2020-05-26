m = xlsread('C:\Users\fabia\Documents\TUD-3\BEP\Code\UI\scenarios.xlsx');
[rows, columns] = size(m);

for row = 1 : rows
   if isnan(m(rows - row + 1, 1))
       m(rows - row + 1, :) = [];
   end
end

t1 = m(1, :);
s1 = m(2, :);
w1 = m(3, :);
d1 = m(4, :);

t2 = m(5, :);
s2 = m(6, :);
w2 = m(7, :);
d2 = m(8, :);

t3 = m(9, :);
s3 = m(10, :);
w3 = m(11, :);
d3 = m(12, :);

t4 = m(13, :);
s4 = m(14, :);
w4 = m(15, :);
d4 = m(16, :);