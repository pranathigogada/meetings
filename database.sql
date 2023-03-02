use flaskapp;

create table participants(
	p_id int not null,
    p_name varchar(30),
    p_mail varchar(50),
    p_ph varchar(10),
    primary key(p_id)
);


insert into participants values (100,"Bindu Madhav","bindumadhavkorrakuti@gmail.com",8919907167),
								(105,"Suresh","suresh2002@gmail.com",9635697841),
                                (110,"Pranathi","pranathi_gogada@srmap.edu.in",9542515049),
                                (115,"Krishna Teja","krishnateja@gmail.com",6304753904),
                                (120,"Harish","harishgolla2003@gmail.com",9182979545),
                                (125,"Rakshitha","rakshitha@gmail.com",9192569356),
                                (130,"Sumanth","sumanth_panguluri@srmap.edu.in",8745632148),
                                (135,"Subhash","subhash_budda@gmail.com",9182979545),
                                (140,"Susmitha","susmitha_edara@srmap.edu.in",7895632145),
                                (145,"Prakash","prakash_avuru@srmap.edu.in",7895632142),
                                (150,"Sohith","sohith_malayala@srmap.edu.in",9705086369),
                                (155,"Dwithin","dwithin_varma@srmap.edu.in",9705086456);
                                
select * from participants;

create table ongoing(
	o_id int not null,
    p_id int not null,
	p_name varchar(30),
    start_time time,
    end_time time,
    foreign key (p_id) references participants (p_id)
);

select * from ongoing;
