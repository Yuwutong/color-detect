%% generate trace of each bbox
clc;
close all;
clear;

src_folder ='D:\data\291-350_C802\txt_10375722802_0920\';
filelist = dir(strcat(src_folder,'*.txt'));
le=length(filelist);
points = cell(1,le);

for ii=1:le
    filename = strcat(src_folder,filelist(ii).name);
    [x,y] = textread(filename,'%n%n');
%     sprintf('x,y = %d,%d',length(x),length(y))
    %points = [points x y];
    points(1,ii) = {[x y]};
%     sprintf('---%d',ii)
end

%% show the trace
% c = linspace(1,10,length(points));
% [~,len] = size(points);
fig = figure;
for jj=1:le
    subplot(4,ceil(le/4),jj)
    title(num2str(jj))
    c = linspace(0,1,length(points{1,jj}));
    a = scatter(points{1,jj}(:,1),points{1,jj}(:,2),[],c);
    axis equal
%     disp(strcat(string(jj),'_', string(jj+1)))
colorbar
end

cd 'D:\data\291-350_C802\'
frame = getframe(fig);
img = frame2im(frame);
imwrite(img,'trace.png')
