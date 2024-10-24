% 数据点
x = [-2, 0, 2, 3, 4, 5, 6, 8, 10, 12, 13, 14, 16, 18];
y = [0, 0.9, 2.0, 6.5, 2.9, 8.8, 3.95, 5.03, 5.97, 7.1, 1.2, 8.2, 8.5, 10.1];

% 参数设置
maxIter = 5000; % 增加迭代次数
threshold = 0.5; % 调整距离阈值，控制内点判定
bestFit = []; % 最好的拟合参数
bestInliersCount = 0; % 内点数量最大值

for i = 1:maxIter
    % 随机选择两个不同的点
    sampleIdx = randperm(length(x), 2);
    x1 = x(sampleIdx(1));
    y1 = y(sampleIdx(1));
    x2 = x(sampleIdx(2));
    y2 = y(sampleIdx(2));
    
    % 计算直线的参数：y = mx + b
    if x2 - x1 == 0
        continue; % 防止除以零的情况
    end
    m = (y2 - y1) / (x2 - x1);
    b = y1 - m * x1;
    
    % 计算所有点到直线的距离
    distances = abs(m * x - y + b) / sqrt(m^2 + 1);
    
    % 统计内点数量
    inliers = distances < threshold;
    inliersCount = sum(inliers);
    
    % 更新最好的拟合结果
    if inliersCount > bestInliersCount
        bestInliersCount = inliersCount;
        bestFit = [m, b];
    end
end

% 输出最好的拟合结果
fprintf('Best fit line: y = %.2fx + %.2f\n', bestFit(1), bestFit(2));

% 绘制原始数据点
figure;
plot(x, y, 'bo', 'MarkerSize', 8, 'DisplayName', 'Data Points');
hold on;

% 绘制拟合的直线
xFit = linspace(min(x), max(x), 100);
yFit = bestFit(1) * xFit + bestFit(2);
plot(xFit, yFit, 'r-', 'LineWidth', 2, 'DisplayName', 'Fitted Line (RANSAC)');

% 设置图形属性
xlabel('x');
ylabel('y');
title('RANSAC Line Fitting');
legend('show');
grid on;
hold off;
