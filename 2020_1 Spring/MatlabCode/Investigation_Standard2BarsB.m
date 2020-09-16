%%


if (0)
i_figure=i_figure+1;
subplot(n_rows, n_cols, i_figure)
hold on
h = bar(1,target_values(1),0.6,'w');
set(h,'FaceColor','r');
h = bar(2,target_values(3),0.6,'w');
set(h,'FaceColor','b');
v_max=min(1,1.2*max(target_values([1,3])));
xticks([])
yticks([0:0.2:1])

if i_figure==3 && v_max==1
    yticks([0:1:8])
    v_max = 1.2*max(target_values([1,3]));
end

if i_figure==6
    v_max=1400;
    v_min = 750;
    yticks([800:200:1600])
end

v_range = v_max-v_min;
axis([0.5 2.5 v_min v_max])
text(1,v_min-0.05*v_range,'Human','HorizontalAlignment','center','FontSize',10,'Interpreter','LaTex')
text(2,v_min-0.05*v_range,'Prediction','HorizontalAlignment','center','FontSize',10,'Interpreter','LaTex')
title(target_title,'Interpreter','LaTex')


else
    
i_figure=i_figure+1;
subplot(n_rows, n_cols, i_figure)
hold on
h = bar(1,target_values(1),0.6,'w');
set(h,'FaceColor','r');
h = bar(2,target_values(3),0.6,'w');
set(h,'FaceColor',[0.5 0.5 0.9]);
h = bar(3,target_values(2),0.6,'w');
set(h,'FaceColor','b');
v_max=min(1,1.2*max(target_values([1,2,3])));
xticks([])
yticks([0:0.2:1])

if i_figure==3 && v_max==1
    yticks([0:1:8])
    v_max = 1.2*max(target_values([1,2,3]));
end

if i_figure==6
    v_max=1400;
    v_min = 750;
    yticks([800:200:1600])
end

v_range = v_max-v_min;
axis([0.5 3.5 v_min v_max])
text(1,v_min-0.05*v_range,'Human','HorizontalAlignment','center','FontSize',10,'Interpreter','LaTex')
text(2,v_min-0.05*v_range,'Certainty','HorizontalAlignment','center','FontSize',10,'Interpreter','LaTex')
text(3,v_min-0.05*v_range,'Unbiased','HorizontalAlignment','center','FontSize',10,'Interpreter','LaTex')
title(target_title,'Interpreter','LaTex')   
    
end
