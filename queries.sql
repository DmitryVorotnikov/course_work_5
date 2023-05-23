CREATE TABLE vacancies
(
	vacancies_id serial,
	title text,
	salary_min int,
	salary_max int,
	currency varchar(10),
	name_company varchar(50),
	link_vacancies text,

	CONSTRAINT pk_vacancies_vacancies_id PRIMARY KEY (vacancies_id)
);
