% CREATE THE FIGURE
figureID=567;
figure(figureID)
hold on
% optimal behavior
plot([0 0.5 0.5 1],[1 1 0 0],'r','LineWidth',3);

% cosmetics
axis([0 1 0 1])
xlabel('Updated Pr(Red Guilty)','Interpreter','Latex')
ylabel('Pr(Investigate Red)','Interpreter','Latex')
%xticks(round(x,2))
xticks([0:0.25:1])
yticks([0:0.25:1])

scale = 1;
set(gcf, 'Position',  [0, 0, 360*scale, 300*scale])
set(gcf,'PaperSize',[7 7]);            %set the paper size
figureNAME = ['MatlabImages/Investigation_Figure',num2str(figureID)];
print(gcf,figureNAME,'-dpdf')          % then print it