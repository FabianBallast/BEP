%m = xlsread('C:\Users\fabia\Documents\TUD-3\BEP\Code\UI\scenarios.xlsx');
%[rows, columns] = size(m);

%for row = 1 : rows
%   if isnan(m(rows - row + 1, 1))
%       m(rows - row + 1, :) = [];
%   end
%end

%t1 = m(1, :);
%s1 = m(2, :);
%w1 = m(3, :);
%d1 = m(4, :);

a = [2, 3];
b = [3, 4];
c = [a; b];