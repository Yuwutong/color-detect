
file_id = '10376945775';
tmp_path = 'D:\OneDrive - City University of Hong Kong\chow\subtract\';
save_dir = strcat(tmp_path,file_id,'\frame\');
% system(['mkdir', ' ', save_dir]);
video_filename = strcat(tmp_path,file_id,'\10376945775(G)-R1-Darkfield-02.mp4');

disp(video_filename)

% file_id = split(video_filename, '\');
% file_id = file_id{end};
% file_id = file_id(1:11);

v = VideoReader(video_filename);
cnt = 1;
while hasFrame(v)
    frame = readFrame(v);
    cnt_str = sprintf('%03d',cnt);
    fprintf([cnt_str,'/400...'])
    frame_name = strcat(save_dir, file_id, '_',cnt_str,'.png');
    imwrite(frame, frame_name)
    cnt = cnt + 1;
    fprintf('\b\b\b\b\b\b\b\b\b\b')
end

