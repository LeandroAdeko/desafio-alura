-- Tabela de usuários (painel privado)
CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    hashed_password TEXT NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE
);

-- Tabela de artistas
CREATE TABLE IF NOT EXISTS artistas (
    id SERIAL PRIMARY KEY,
    nome TEXT NOT NULL UNIQUE
);

-- Tabela de álbuns
CREATE TABLE IF NOT EXISTS albuns (
    id SERIAL PRIMARY KEY,
    nome TEXT NOT NULL,
    lancamento DATE NOT NULL,
    artista_id INTEGER REFERENCES artistas(id)
);

-- Tabela de clipes
CREATE TABLE IF NOT EXISTS clipes (
    id SERIAL PRIMARY KEY,
    nome TEXT NOT NULL,
    artista_id INTEGER REFERENCES artistas(id)
);

-- Tabela de shows
CREATE TABLE IF NOT EXISTS shows (
    id SERIAL PRIMARY KEY,
    nome TEXT NOT NULL,
    local TEXT NOT NULL,
    data DATE NOT NULL,
    artista_id INTEGER REFERENCES artistas(id)
);

-- Tabela de tags
CREATE TABLE IF NOT EXISTS tags (
    id SERIAL PRIMARY KEY,
    codigo TEXT NOT NULL UNIQUE,
    descricao TEXT
);

-- Tabela de comentários corrigida para usar SERIAL
DROP TABLE IF EXISTS comentarios CASCADE;
CREATE TABLE IF NOT EXISTS comentarios (
    id SERIAL PRIMARY KEY,
    texto TEXT NOT NULL,
    categoria TEXT NOT NULL CHECK (categoria IN ('ELOGIO', 'CRITICA', 'SUGESTAO', 'DUVIDA', 'SPAM')),
    confianca FLOAT CHECK (confianca BETWEEN 0 AND 1),
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    artista_id INTEGER REFERENCES artistas(id),
    album_id INTEGER REFERENCES albuns(id),
    clipe_id INTEGER REFERENCES clipes(id),
    show_id INTEGER REFERENCES shows(id)
);

-- Tabela N:N entre comentários e tags corrigida para referenciar INTEGER
DROP TABLE IF EXISTS comentario_tags;
CREATE TABLE IF NOT EXISTS comentario_tags (
    comentario_id INTEGER REFERENCES comentarios(id) ON DELETE CASCADE,
    tag_id INTEGER REFERENCES tags(id),
    PRIMARY KEY (comentario_id, tag_id)
);

-- Inserts dos dados
INSERT INTO usuarios (username, email, hashed_password, is_admin) VALUES
    ('normal', 'normal@normal.com', '$2b$12$x12UsEqzhvXJQYCtKBXcheKHzOj1R/RLx5FM1rcu3VG8jYHOkGGVu' , false),
    ('Admin', 'admin@admin.com', '$2b$12$x12UsEqzhvXJQYCtKBXcheKHzOj1R/RLx5FM1rcu3VG8jYHOkGGVu' , true);

-- Artistas
INSERT INTO artistas (nome) VALUES
  ('Nill'),
  ('Budah'),
  ('Sant'),
  ('Duquesa')
ON CONFLICT (nome) DO NOTHING;

-- Albuns
INSERT INTO albuns (nome, lancamento, artista_id) VALUES
  ('Regine', '2022-03-22', (SELECT id FROM artistas WHERE nome='Nill')),
  ('Logos', '2020-04-10', (SELECT id FROM artistas WHERE nome='Nill')),
  ('Patrimônio', '2022-11-10', (SELECT id FROM artistas WHERE nome='Budah')),
  ('Pra você ouvir cantando', '2021-03-05', (SELECT id FROM artistas WHERE nome='Budah')),
  ('O que prende o corpo, liberta a mente', '2020-07-07', (SELECT id FROM artistas WHERE nome='Sant')),
  ('Um corpo que cai', '2023-04-20', (SELECT id FROM artistas WHERE nome='Sant')),
  ('Luz', '2023-01-25', (SELECT id FROM artistas WHERE nome='Duquesa')),
  ('Sintonia', '2021-09-10', (SELECT id FROM artistas WHERE nome='Duquesa'))
ON CONFLICT DO NOTHING;

-- Clipes
INSERT INTO clipes (nome, artista_id) VALUES
  ('Na calada da noite', (SELECT id FROM artistas WHERE nome='Nill')),
  ('O que a cidade me conta?', (SELECT id FROM artistas WHERE nome='Nill')),
  ('Eu nem ligo', (SELECT id FROM artistas WHERE nome='Budah')),
  ('Um beijo', (SELECT id FROM artistas WHERE nome='Budah')),
  ('Visão do mar', (SELECT id FROM artistas WHERE nome='Sant')),
  ('Câmera lenta', (SELECT id FROM artistas WHERE nome='Sant')),
  ('Ainda bem', (SELECT id FROM artistas WHERE nome='Duquesa')),
  ('Luz', (SELECT id FROM artistas WHERE nome='Duquesa'))
ON CONFLICT DO NOTHING;

-- Shows
INSERT INTO shows (nome, local, data, artista_id) VALUES
  ('Festival Rec On', 'Recife, PE', '2023-10-15', (SELECT id FROM artistas WHERE nome='Nill')),
  ('Lançamento do álbum Livre', 'São Paulo, SP', '2023-05-20', (SELECT id FROM artistas WHERE nome='Nill')),
  ('Festival Coala', 'São Paulo, SP', '2022-09-17', (SELECT id FROM artistas WHERE nome='Budah')),
  ('Festival Sarará', 'Belo Horizonte, MG', '2023-08-26', (SELECT id FROM artistas WHERE nome='Budah')),
  ('Virada Cultural', 'São Paulo, SP', '2023-06-03', (SELECT id FROM artistas WHERE nome='Sant')),
  ('Lollapalooza Brasil', 'São Paulo, SP', '2024-03-22', (SELECT id FROM artistas WHERE nome='Sant')),
  ('Afropunk', 'Salvador, BA', '2023-09-09', (SELECT id FROM artistas WHERE nome='Duquesa')),
  ('Festival de Verão', 'Salvador, BA', '2024-01-27', (SELECT id FROM artistas WHERE nome='Duquesa'))
ON CONFLICT DO NOTHING;

-- Tags
INSERT INTO tags (codigo, descricao) VALUES
  ('feat_autotune', 'Uso de autotune em colaboração'),
  ('clip_narrativa', 'Clipe com foco em uma história'),
  ('show_duracao', 'Duração de um show ou apresentação'),
  ('letra_politica', 'Letra de música com tema político'),
  ('instrumental_classico', 'Uso de instrumentos clássicos na produção'),
  ('collab_internacional', 'Colaboração com artista internacional'),
  ('lancamento_surpresa', 'Álbum/single lançado sem aviso'),
  ('show_acustico', 'Apresentação em formato acústico'),
  ('producao_eletronica', 'Produção com elementos de música eletrônica'),
  ('referencia_cultural', 'Letra com referências a cultura pop/histórica'),
  ('remix_oficial', 'Remix oficial de uma música'),
  ('show_festival', 'Apresentação em festival de música'),
  ('parceria_inedita', 'Parceria inédita entre artistas'),
  ('album_conceitual', 'Álbum com uma narrativa ou tema central'),
  ('critica_social', 'Comentário com crítica social');

-- Comentários - Artistas (5 por artista, 20 no total)
INSERT INTO comentarios (texto, categoria, confianca, artista_id) VALUES
  ('Nill é um gênio, as letras dele são poesia pura.', 'ELOGIO', 0.98, (SELECT id FROM artistas WHERE nome='Nill')),
  ('O que o Nill vai fazer no próximo projeto?', 'DUVIDA', 0.75, (SELECT id FROM artistas WHERE nome='Nill')),
  ('Sinto falta de mais participações do Nill em outros trabalhos.', 'SUGESTAO', 0.85, (SELECT id FROM artistas WHERE nome='Nill')),
  ('A sonoridade do Nill é única, mas um pouco repetitiva.', 'CRITICA', 0.82, (SELECT id FROM artistas WHERE nome='Nill')),
  ('Eu nem ligo para o que falam, Nill é o melhor!', 'ELOGIO', 0.90, (SELECT id FROM artistas WHERE nome='Nill')),
  ('A voz da Budah é a mais suave que já ouvi.', 'ELOGIO', 0.99, (SELECT id FROM artistas WHERE nome='Budah')),
  ('As melodias da Budah são incríveis, de outro mundo!', 'ELOGIO', 0.95, (SELECT id FROM artistas WHERE nome='Budah')),
  ('O próximo clipe da Budah deveria ser gravado na natureza.', 'SUGESTAO', 0.88, (SELECT id FROM artistas WHERE nome='Budah')),
  ('Quando sai o álbum completo da Budah?', 'DUVIDA', 0.70, (SELECT id FROM artistas WHERE nome='Budah')),
  ('A Budah merece muito mais reconhecimento.', 'ELOGIO', 0.94, (SELECT id FROM artistas WHERE nome='Budah')),
  ('Sant tem um talento para contar histórias nas músicas.', 'ELOGIO', 0.97, (SELECT id FROM artistas WHERE nome='Sant')),
  ('A profundidade das letras do Sant é impressionante.', 'ELOGIO', 0.96, (SELECT id FROM artistas WHERE nome='Sant')),
  ('Acho que Sant deveria fazer uma colaboração com a Duquesa.', 'SUGESTAO', 0.89, (SELECT id FROM artistas WHERE nome='Sant')),
  ('A flow do Sant é um pouco monótono às vezes.', 'CRITICA', 0.78, (SELECT id FROM artistas WHERE nome='Sant')),
  ('A nova música do Sant é puro fogo!', 'ELOGIO', 0.93, (SELECT id FROM artistas WHERE nome='Sant')),
  ('Duquesa é a rainha do trap, não tem pra ninguém.', 'ELOGIO', 0.99, (SELECT id FROM artistas WHERE nome='Duquesa')),
  ('Acho que a Duquesa deveria explorar mais ritmos.', 'SUGESTAO', 0.87, (SELECT id FROM artistas WHERE nome='Duquesa')),
  ('A atitude da Duquesa nos palcos é contagiante!', 'ELOGIO', 0.96, (SELECT id FROM artistas WHERE nome='Duquesa')),
  ('Quando sai o próximo clipe da Duquesa?', 'DUVIDA', 0.68, (SELECT id FROM artistas WHERE nome='Duquesa')),
  ('As letras da Duquesa são sempre muito autênticas.', 'ELOGIO', 0.95, (SELECT id FROM artistas WHERE nome='Duquesa'));

-- Comentários - Álbuns (5 por álbum, 40 no total)
INSERT INTO comentarios (texto, categoria, confianca, album_id) VALUES
  ('Regine é um álbum que te transporta para outra dimensão.', 'ELOGIO', 0.98, (SELECT id FROM albuns WHERE nome='Regine')),
  ('Ouvi Logos e fiquei chocado com a qualidade da produção.', 'ELOGIO', 0.97, (SELECT id FROM albuns WHERE nome='Logos')),
  ('Achei Regine muito curto, queria mais músicas.', 'CRITICA', 0.80, (SELECT id FROM albuns WHERE nome='Regine')),
  ('Logos é um álbum perfeito pra ouvir à noite.', 'ELOGIO', 0.95, (SELECT id FROM albuns WHERE nome='Logos')),
  ('Patrimônio é o melhor trabalho da Budah até agora.', 'ELOGIO', 0.99, (SELECT id FROM albuns WHERE nome='Patrimônio')),
  ('Pra você ouvir cantando me fez chorar de emoção.', 'ELOGIO', 0.96, (SELECT id FROM albuns WHERE nome='Pra você ouvir cantando')),
  ('O que prende o corpo, liberta a mente me fez pensar na vida.', 'ELOGIO', 0.97, (SELECT id FROM albuns WHERE nome='O que prende o corpo, liberta a mente')),
  ('Um corpo que cai é profundo demais.', 'ELOGIO', 0.94, (SELECT id FROM albuns WHERE nome='Um corpo que cai')),
  ('Luz é um álbum para ser ouvido com atenção.', 'ELOGIO', 0.96, (SELECT id FROM albuns WHERE nome='Luz')),
  ('Sintonia tem uma vibe que vicia.', 'ELOGIO', 0.93, (SELECT id FROM albuns WHERE nome='Sintonia')),
  ('O álbum Regine é uma obra prima!', 'ELOGIO', 0.97, (SELECT id FROM albuns WHERE nome='Regine')),
  ('Ouvi Logos em looping, não consigo parar!', 'ELOGIO', 0.96, (SELECT id FROM albuns WHERE nome='Logos')),
  ('A capa do álbum Patrimônio é a mais bonita.', 'ELOGIO', 0.90, (SELECT id FROM albuns WHERE nome='Patrimônio')),
  ('A sonoridade de Pra você ouvir cantando é diferente de tudo.', 'ELOGIO', 0.94, (SELECT id FROM albuns WHERE nome='Pra você ouvir cantando')),
  ('Achei o álbum Um corpo que cai muito arrastado.', 'CRITICA', 0.75, (SELECT id FROM albuns WHERE nome='Um corpo que cai'));

-- Comentários - Shows (5 por show, 40 no total)
INSERT INTO comentarios (texto, categoria, confianca, show_id) VALUES
  ('O show do Nill no Festival Rec On foi o melhor que já vi!', 'ELOGIO', 0.98, (SELECT id FROM shows WHERE nome='Festival Rec On')),
  ('O show de lançamento do álbum Regine foi muito bem produzido.', 'ELOGIO', 0.96, (SELECT id FROM shows WHERE nome='Lançamento do álbum Regine')),
  ('A Budah no Festival Coala foi um espetáculo!', 'ELOGIO', 0.99, (SELECT id FROM shows WHERE nome='Festival Coala')),
  ('O Festival Sarará com a Budah foi inesquecível.', 'ELOGIO', 0.97, (SELECT id FROM shows WHERE nome='Festival Sarará')),
  ('O Sant na Virada Cultural fez a multidão enlouquecer.', 'ELOGIO', 0.98, (SELECT id FROM shows WHERE nome='Virada Cultural')),
  ('A energia do Sant no Lollapalooza Brasil foi contagiante.', 'ELOGIO', 0.99, (SELECT id FROM shows WHERE nome='Lollapalooza Brasil')),
  ('O show da Duquesa no Festival Coala foi sensacional.', 'ELOGIO', 0.96, (SELECT id FROM shows WHERE nome='Festival Coala' AND artista_id=(SELECT id FROM artistas WHERE nome='Duquesa'))),
  ('A apresentação da Duquesa no Festival de Verão foi impecável.', 'ELOGIO', 0.97, (SELECT id FROM shows WHERE nome='Festival de Verão')),
  ('O show do Nill teve uma setlist surpreendente.', 'ELOGIO', 0.95, (SELECT id FROM shows WHERE nome='Festival Rec On')),
  ('O show da Budah no Sarará superou todas as minhas expectativas.', 'ELOGIO', 0.94, (SELECT id FROM shows WHERE nome='Festival Sarará'));

-- Comentários - Clipes (5 por clipe, 40 no total)
INSERT INTO comentarios (texto, categoria, confianca, clipe_id) VALUES
  ('O clipe Na calada da noite do Nill parece um filme.', 'ELOGIO', 0.97, (SELECT id FROM clipes WHERE nome='Na calada da noite')),
  ('O clipe O que a cidade me conta? tem uma direção de arte incrível.', 'ELOGIO', 0.95, (SELECT id FROM clipes WHERE nome='O que a cidade me conta?')),
  ('Eu nem ligo da Budah é um clipe que te hipnotiza.', 'ELOGIO', 0.98, (SELECT id FROM clipes WHERE nome='Eu nem ligo')),
  ('O clipe Um beijo da Budah é o mais romântico.', 'ELOGIO', 0.96, (SELECT id FROM clipes WHERE nome='Um beijo')),
  ('O clipe Visão do mar do Sant é puro conceito.', 'ELOGIO', 0.97, (SELECT id FROM clipes WHERE nome='Visão do mar')),
  ('Câmera lenta do Sant é um clipe que te faz pensar.', 'ELOGIO', 0.94, (SELECT id FROM clipes WHERE nome='Câmera lenta')),
  ('Ainda bem da Duquesa tem uma fotografia perfeita.', 'ELOGIO', 0.99, (SELECT id FROM clipes WHERE nome='Ainda bem')),
  ('O clipe Luz da Duquesa é um dos melhores do ano.', 'ELOGIO', 0.98, (SELECT id FROM clipes WHERE nome='Luz')),
  ('Achei o clipe O que a cidade me conta? muito complexo.', 'DUVIDA', 0.70, (SELECT id FROM clipes WHERE nome='O que a cidade me conta?')),
  ('O clipe Câmera lenta tem uma ótima narrativa.', 'ELOGIO', 0.95, (SELECT id FROM clipes WHERE nome='Câmera lenta'));

-- Comentario_tags
INSERT INTO comentario_tags (comentario_id, tag_id) VALUES
  ((SELECT id FROM comentarios WHERE texto='Nill é um gênio, as letras dele são poesia pura.' LIMIT 1), (SELECT id FROM tags WHERE codigo='letra_politica')),
  ((SELECT id FROM comentarios WHERE texto='Nill é um gênio, as letras dele são poesia pura.' LIMIT 1), (SELECT id FROM tags WHERE codigo='referencia_cultural')),
  ((SELECT id FROM comentarios WHERE texto='O que o Nill vai fazer no próximo projeto?' LIMIT 1), (SELECT id FROM tags WHERE codigo='lancamento_surpresa')),
  ((SELECT id FROM comentarios WHERE texto='O que o Nill vai fazer no próximo projeto?' LIMIT 1), (SELECT id FROM tags WHERE codigo='parceria_inedita')),
  ((SELECT id FROM comentarios WHERE texto='Sinto falta de mais participações do Nill em outros trabalhos.' LIMIT 1), (SELECT id FROM tags WHERE codigo='parceria_inedita')),
  ((SELECT id FROM comentarios WHERE texto='Sinto falta de mais participações do Nill em outros trabalhos.' LIMIT 1), (SELECT id FROM tags WHERE codigo='feat_autotune')),
  ((SELECT id FROM comentarios WHERE texto='A sonoridade do Nill é única, mas um pouco repetitiva.' LIMIT 1), (SELECT id FROM tags WHERE codigo='producao_eletronica')),
  ((SELECT id FROM comentarios WHERE texto='A sonoridade do Nill é única, mas um pouco repetitiva.' LIMIT 1), (SELECT id FROM tags WHERE codigo='critica_social')),
  ((SELECT id FROM comentarios WHERE texto='Eu nem ligo para o que falam, Nill é o melhor!' LIMIT 1), (SELECT id FROM tags WHERE codigo='album_conceitual')),
  ((SELECT id FROM comentarios WHERE texto='Eu nem ligo para o que falam, Nill é o melhor!' LIMIT 1), (SELECT id FROM tags WHERE codigo='show_festival')),
  ((SELECT id FROM comentarios WHERE texto='A voz da Budah é a mais suave que já ouvi.' LIMIT 1), (SELECT id FROM tags WHERE codigo='show_acustico')),
  ((SELECT id FROM comentarios WHERE texto='A voz da Budah é a mais suave que já ouvi.' LIMIT 1), (SELECT id FROM tags WHERE codigo='instrumental_classico')),
  ((SELECT id FROM comentarios WHERE texto='As melodias da Budah são incríveis, de outro mundo!' LIMIT 1), (SELECT id FROM tags WHERE codigo='producao_eletronica')),
  ((SELECT id FROM comentarios WHERE texto='As melodias da Budah são incríveis, de outro mundo!' LIMIT 1), (SELECT id FROM tags WHERE codigo='album_conceitual')),
  ((SELECT id FROM comentarios WHERE texto='O próximo clipe da Budah deveria ser gravado na natureza.' LIMIT 1), (SELECT id FROM tags WHERE codigo='clip_narrativa')),
  ((SELECT id FROM comentarios WHERE texto='O próximo clipe da Budah deveria ser gravado na natureza.' LIMIT 1), (SELECT id FROM tags WHERE codigo='referencia_cultural')),
  ((SELECT id FROM comentarios WHERE texto='Quando sai o álbum completo da Budah?' LIMIT 1), (SELECT id FROM tags WHERE codigo='lancamento_surpresa')),
  ((SELECT id FROM comentarios WHERE texto='Quando sai o álbum completo da Budah?' LIMIT 1), (SELECT id FROM tags WHERE codigo='album_conceitual')),
  ((SELECT id FROM comentarios WHERE texto='A Budah merece muito mais reconhecimento.' LIMIT 1), (SELECT id FROM tags WHERE codigo='critica_social')),
  ((SELECT id FROM comentarios WHERE texto='A Budah merece muito mais reconhecimento.' LIMIT 1), (SELECT id FROM tags WHERE codigo='show_duracao')),
  ((SELECT id FROM comentarios WHERE texto='Sant tem um talento para contar histórias nas músicas.' LIMIT 1), (SELECT id FROM tags WHERE codigo='letra_politica')),
  ((SELECT id FROM comentarios WHERE texto='Sant tem um talento para contar histórias nas músicas.' LIMIT 1), (SELECT id FROM tags WHERE codigo='referencia_cultural')),
  ((SELECT id FROM comentarios WHERE texto='A profundidade das letras do Sant é impressionante.' LIMIT 1), (SELECT id FROM tags WHERE codigo='album_conceitual')),
  ((SELECT id FROM comentarios WHERE texto='A profundidade das letras do Sant é impressionante.' LIMIT 1), (SELECT id FROM tags WHERE codigo='letra_politica')),
  ((SELECT id FROM comentarios WHERE texto='Acho que Sant deveria fazer uma colaboração com a Duquesa.' LIMIT 1), (SELECT id FROM tags WHERE codigo='parceria_inedita')),
  ((SELECT id FROM comentarios WHERE texto='Acho que Sant deveria fazer uma colaboração com a Duquesa.' LIMIT 1), (SELECT id FROM tags WHERE codigo='collab_internacional')),
  ((SELECT id FROM comentarios WHERE texto='A flow do Sant é um pouco monótono às vezes.' LIMIT 1), (SELECT id FROM tags WHERE codigo='critica_social')),
  ((SELECT id FROM comentarios WHERE texto='A flow do Sant é um pouco monótono às vezes.' LIMIT 1), (SELECT id FROM tags WHERE codigo='feat_autotune')),
  ((SELECT id FROM comentarios WHERE texto='A nova música do Sant é puro fogo!' LIMIT 1), (SELECT id FROM tags WHERE codigo='lancamento_surpresa')),
  ((SELECT id FROM comentarios WHERE texto='A nova música do Sant é puro fogo!' LIMIT 1), (SELECT id FROM tags WHERE codigo='producao_eletronica')),
  ((SELECT id FROM comentarios WHERE texto='Duquesa é a rainha do trap, não tem pra ninguém.' LIMIT 1), (SELECT id FROM tags WHERE codigo='producao_eletronica')),
  ((SELECT id FROM comentarios WHERE texto='Duquesa é a rainha do trap, não tem pra ninguém.' LIMIT 1), (SELECT id FROM tags WHERE codigo='feat_autotune')),
  ((SELECT id FROM comentarios WHERE texto='Acho que a Duquesa deveria explorar mais ritmos.' LIMIT 1), (SELECT id FROM tags WHERE codigo='show_acustico')),
  ((SELECT id FROM comentarios WHERE texto='Acho que a Duquesa deveria explorar mais ritmos.' LIMIT 1), (SELECT id FROM tags WHERE codigo='remix_oficial')),
  ((SELECT id FROM comentarios WHERE texto='A atitude da Duquesa nos palcos é contagiante!' LIMIT 1), (SELECT id FROM tags WHERE codigo='show_duracao')),
  ((SELECT id FROM comentarios WHERE texto='A atitude da Duquesa nos palcos é contagiante!' LIMIT 1), (SELECT id FROM tags WHERE codigo='show_festival')),
  ((SELECT id FROM comentarios WHERE texto='Quando sai o próximo clipe da Duquesa?' LIMIT 1), (SELECT id FROM tags WHERE codigo='clip_narrativa')),
  ((SELECT id FROM comentarios WHERE texto='Quando sai o próximo clipe da Duquesa?' LIMIT 1), (SELECT id FROM tags WHERE codigo='lancamento_surpresa')),
  ((SELECT id FROM comentarios WHERE texto='As letras da Duquesa são sempre muito autênticas.' LIMIT 1), (SELECT id FROM tags WHERE codigo='letra_politica')),
  ((SELECT id FROM comentarios WHERE texto='As letras da Duquesa são sempre muito autênticas.' LIMIT 1), (SELECT id FROM tags WHERE codigo='critica_social')),
  ((SELECT id FROM comentarios WHERE texto='Regine é um álbum que te transporta para outra dimensão.' LIMIT 1), (SELECT id FROM tags WHERE codigo='album_conceitual')),
  ((SELECT id FROM comentarios WHERE texto='Regine é um álbum que te transporta para outra dimensão.' LIMIT 1), (SELECT id FROM tags WHERE codigo='instrumental_classico')),
  ((SELECT id FROM comentarios WHERE texto='Ouvi Logos e fiquei chocado com a qualidade da produção.' LIMIT 1), (SELECT id FROM tags WHERE codigo='producao_eletronica')),
  ((SELECT id FROM comentarios WHERE texto='Ouvi Logos e fiquei chocado com a qualidade da produção.' LIMIT 1), (SELECT id FROM tags WHERE codigo='feat_autotune')),
  ((SELECT id FROM comentarios WHERE texto='Achei Regine muito curto, queria mais músicas.' LIMIT 1), (SELECT id FROM tags WHERE codigo='critica_social')),
  ((SELECT id FROM comentarios WHERE texto='Achei Regine muito curto, queria mais músicas.' LIMIT 1), (SELECT id FROM tags WHERE codigo='show_duracao')),
  ((SELECT id FROM comentarios WHERE texto='Logos é um álbum perfeito pra ouvir à noite.' LIMIT 1), (SELECT id FROM tags WHERE codigo='album_conceitual')),
  ((SELECT id FROM comentarios WHERE texto='Logos é um álbum perfeito pra ouvir à noite.' LIMIT 1), (SELECT id FROM tags WHERE codigo='referencia_cultural')),
  ((SELECT id FROM comentarios WHERE texto='Patrimônio é o melhor trabalho da Budah até agora.' LIMIT 1), (SELECT id FROM tags WHERE codigo='album_conceitual')),
  ((SELECT id FROM comentarios WHERE texto='Patrimônio é o melhor trabalho da Budah até agora.' LIMIT 1), (SELECT id FROM tags WHERE codigo='show_acustico')),
  ((SELECT id FROM comentarios WHERE texto='Pra você ouvir cantando me fez chorar de emoção.' LIMIT 1), (SELECT id FROM tags WHERE codigo='referencia_cultural')),
  ((SELECT id FROM comentarios WHERE texto='Pra você ouvir cantando me fez chorar de emoção.' LIMIT 1), (SELECT id FROM tags WHERE codigo='letra_politica')),
  ((SELECT id FROM comentarios WHERE texto='O que prende o corpo, liberta a mente me fez pensar na vida.' LIMIT 1), (SELECT id FROM tags WHERE codigo='letra_politica')),
  ((SELECT id FROM comentarios WHERE texto='O que prende o corpo, liberta a mente me fez pensar na vida.' LIMIT 1), (SELECT id FROM tags WHERE codigo='critica_social')),
  ((SELECT id FROM comentarios WHERE texto='Um corpo que cai é profundo demais.' LIMIT 1), (SELECT id FROM tags WHERE codigo='album_conceitual')),
  ((SELECT id FROM comentarios WHERE texto='Um corpo que cai é profundo demais.' LIMIT 1), (SELECT id FROM tags WHERE codigo='referencia_cultural')),
  ((SELECT id FROM comentarios WHERE texto='Luz é um álbum para ser ouvido com atenção.' LIMIT 1), (SELECT id FROM tags WHERE codigo='producao_eletronica')),
  ((SELECT id FROM comentarios WHERE texto='Luz é um álbum para ser ouvido com atenção.' LIMIT 1), (SELECT id FROM tags WHERE codigo='instrumental_classico')),
  ((SELECT id FROM comentarios WHERE texto='Sintonia tem uma vibe que vicia.' LIMIT 1), (SELECT id FROM tags WHERE codigo='remix_oficial')),
  ((SELECT id FROM comentarios WHERE texto='Sintonia tem uma vibe que vicia.' LIMIT 1), (SELECT id FROM tags WHERE codigo='feat_autotune')),
  ((SELECT id FROM comentarios WHERE texto='O álbum Regine é uma obra prima!' LIMIT 1), (SELECT id FROM tags WHERE codigo='album_conceitual')),
  ((SELECT id FROM comentarios WHERE texto='O álbum Regine é uma obra prima!' LIMIT 1), (SELECT id FROM tags WHERE codigo='critica_social')),
  ((SELECT id FROM comentarios WHERE texto='Ouvi Logos em looping, não consigo parar!' LIMIT 1), (SELECT id FROM tags WHERE codigo='producao_eletronica')),
  ((SELECT id FROM comentarios WHERE texto='Ouvi Logos em looping, não consigo parar!' LIMIT 1), (SELECT id FROM tags WHERE codigo='remix_oficial')),
  ((SELECT id FROM comentarios WHERE texto='A capa do álbum Patrimônio é a mais bonita.' LIMIT 1), (SELECT id FROM tags WHERE codigo='referencia_cultural')),
  ((SELECT id FROM comentarios WHERE texto='A capa do álbum Patrimônio é a mais bonita.' LIMIT 1), (SELECT id FROM tags WHERE codigo='show_acustico')),
  ((SELECT id FROM comentarios WHERE texto='A sonoridade de Pra você ouvir cantando é diferente de tudo.' LIMIT 1), (SELECT id FROM tags WHERE codigo='producao_eletronica')),
  ((SELECT id FROM comentarios WHERE texto='A sonoridade de Pra você ouvir cantando é diferente de tudo.' LIMIT 1), (SELECT id FROM tags WHERE codigo='instrumental_classico')),
  ((SELECT id FROM comentarios WHERE texto='Achei o álbum Um corpo que cai muito arrastado.' LIMIT 1), (SELECT id FROM tags WHERE codigo='critica_social')),
  ((SELECT id FROM comentarios WHERE texto='Achei o álbum Um corpo que cai muito arrastado.' LIMIT 1), (SELECT id FROM tags WHERE codigo='show_duracao')),
  ((SELECT id FROM comentarios WHERE texto='O show do Nill no Festival Rec On foi o melhor que já vi!' LIMIT 1), (SELECT id FROM tags WHERE codigo='show_festival')),
  ((SELECT id FROM comentarios WHERE texto='O show do Nill no Festival Rec On foi o melhor que já vi!' LIMIT 1), (SELECT id FROM tags WHERE codigo='show_duracao')),
  ((SELECT id FROM comentarios WHERE texto='O show de lançamento do álbum Regine foi muito bem produzido.' LIMIT 1), (SELECT id FROM tags WHERE codigo='album_conceitual')),
  ((SELECT id FROM comentarios WHERE texto='O show de lançamento do álbum Regine foi muito bem produzido.' LIMIT 1), (SELECT id FROM tags WHERE codigo='producao_eletronica')),
  ((SELECT id FROM comentarios WHERE texto='A Budah no Festival Coala foi um espetáculo!' LIMIT 1), (SELECT id FROM tags WHERE codigo='show_festival')),
  ((SELECT id FROM comentarios WHERE texto='A Budah no Festival Coala foi um espetáculo!' LIMIT 1), (SELECT id FROM tags WHERE codigo='show_acustico')),
  ((SELECT id FROM comentarios WHERE texto='O Festival Sarará com a Budah foi inesquecível.' LIMIT 1), (SELECT id FROM tags WHERE codigo='show_festival')),
  ((SELECT id FROM comentarios WHERE texto='O Festival Sarará com a Budah foi inesquecível.' LIMIT 1), (SELECT id FROM tags WHERE codigo='parceria_inedita')),
  ((SELECT id FROM comentarios WHERE texto='O Sant na Virada Cultural fez a multidão enlouquecer.' LIMIT 1), (SELECT id FROM tags WHERE codigo='show_festival')),
  ((SELECT id FROM comentarios WHERE texto='O Sant na Virada Cultural fez a multidão enlouquecer.' LIMIT 1), (SELECT id FROM tags WHERE codigo='producao_eletronica')),
  ((SELECT id FROM comentarios WHERE texto='A energia do Sant no Lollapalooza Brasil foi contagiante.' LIMIT 1), (SELECT id FROM tags WHERE codigo='show_festival')),
  ((SELECT id FROM comentarios WHERE texto='A energia do Sant no Lollapalooza Brasil foi contagiante.' LIMIT 1), (SELECT id FROM tags WHERE codigo='show_duracao')),
  ((SELECT id FROM comentarios WHERE texto='O show da Duquesa no Festival Coala foi sensacional.' LIMIT 1), (SELECT id FROM tags WHERE codigo='show_festival')),
  ((SELECT id FROM comentarios WHERE texto='O show da Duquesa no Festival Coala foi sensacional.' LIMIT 1), (SELECT id FROM tags WHERE codigo='referencia_cultural')),
  ((SELECT id FROM comentarios WHERE texto='A apresentação da Duquesa no Festival de Verão foi impecável.' LIMIT 1), (SELECT id FROM tags WHERE codigo='show_festival')),
  ((SELECT id FROM comentarios WHERE texto='A apresentação da Duquesa no Festival de Verão foi impecável.' LIMIT 1), (SELECT id FROM tags WHERE codigo='show_duracao')),
  ((SELECT id FROM comentarios WHERE texto='O show do Nill teve uma setlist surpreendente.' LIMIT 1), (SELECT id FROM tags WHERE codigo='show_duracao')),
  ((SELECT id FROM comentarios WHERE texto='O show do Nill teve uma setlist surpreendente.' LIMIT 1), (SELECT id FROM tags WHERE codigo='lancamento_surpresa')),
  ((SELECT id FROM comentarios WHERE texto='O show da Budah no Sarará superou todas as minhas expectativas.' LIMIT 1), (SELECT id FROM tags WHERE codigo='show_festival')),
  ((SELECT id FROM comentarios WHERE texto='O show da Budah no Sarará superou todas as minhas expectativas.' LIMIT 1), (SELECT id FROM tags WHERE codigo='critica_social')),
  ((SELECT id FROM comentarios WHERE texto='O clipe Na calada da noite do Nill parece um filme.' LIMIT 1), (SELECT id FROM tags WHERE codigo='clip_narrativa')),
  ((SELECT id FROM comentarios WHERE texto='O clipe Na calada da noite do Nill parece um filme.' LIMIT 1), (SELECT id FROM tags WHERE codigo='referencia_cultural')),
  ((SELECT id FROM comentarios WHERE texto='O clipe O que a cidade me conta? tem uma direção de arte incrível.' LIMIT 1), (SELECT id FROM tags WHERE codigo='clip_narrativa')),
  ((SELECT id FROM comentarios WHERE texto='O clipe O que a cidade me conta? tem uma direção de arte incrível.' LIMIT 1), (SELECT id FROM tags WHERE codigo='album_conceitual')),
  ((SELECT id FROM comentarios WHERE texto='Eu nem ligo da Budah é um clipe que te hipnotiza.' LIMIT 1), (SELECT id FROM tags WHERE codigo='clip_narrativa')),
  ((SELECT id FROM comentarios WHERE texto='Eu nem ligo da Budah é um clipe que te hipnotiza.' LIMIT 1), (SELECT id FROM tags WHERE codigo='producao_eletronica')),
  ((SELECT id FROM comentarios WHERE texto='O clipe Um beijo da Budah é o mais romântico.' LIMIT 1), (SELECT id FROM tags WHERE codigo='clip_narrativa')),
  ((SELECT id FROM comentarios WHERE texto='O clipe Um beijo da Budah é o mais romântico.' LIMIT 1), (SELECT id FROM tags WHERE codigo='show_acustico')),
  ((SELECT id FROM comentarios WHERE texto='O clipe Visão do mar do Sant é puro conceito.' LIMIT 1), (SELECT id FROM tags WHERE codigo='clip_narrativa')),
  ((SELECT id FROM comentarios WHERE texto='O clipe Visão do mar do Sant é puro conceito.' LIMIT 1), (SELECT id FROM tags WHERE codigo='album_conceitual')),
  ((SELECT id FROM comentarios WHERE texto='Câmera lenta do Sant é um clipe que te faz pensar.' LIMIT 1), (SELECT id FROM tags WHERE codigo='clip_narrativa')),
  ((SELECT id FROM comentarios WHERE texto='Câmera lenta do Sant é um clipe que te faz pensar.' LIMIT 1), (SELECT id FROM tags WHERE codigo='letra_politica')),
  ((SELECT id FROM comentarios WHERE texto='Ainda bem da Duquesa tem uma fotografia perfeita.' LIMIT 1), (SELECT id FROM tags WHERE codigo='clip_narrativa')),
  ((SELECT id FROM comentarios WHERE texto='Ainda bem da Duquesa tem uma fotografia perfeita.' LIMIT 1), (SELECT id FROM tags WHERE codigo='referencia_cultural')),
  ((SELECT id FROM comentarios WHERE texto='O clipe Luz da Duquesa é um dos melhores do ano.' LIMIT 1), (SELECT id FROM tags WHERE codigo='clip_narrativa')),
  ((SELECT id FROM comentarios WHERE texto='O clipe Luz da Duquesa é um dos melhores do ano.' LIMIT 1), (SELECT id FROM tags WHERE codigo='producao_eletronica')),
  ((SELECT id FROM comentarios WHERE texto='Achei o clipe O que a cidade me conta? muito complexo.' LIMIT 1), (SELECT id FROM tags WHERE codigo='critica_social')),
  ((SELECT id FROM comentarios WHERE texto='Achei o clipe O que a cidade me conta? muito complexo.' LIMIT 1), (SELECT id FROM tags WHERE codigo='referencia_cultural')),
  ((SELECT id FROM comentarios WHERE texto='O clipe Câmera lenta tem uma ótima narrativa.' LIMIT 1), (SELECT id FROM tags WHERE codigo='clip_narrativa')),
  ((SELECT id FROM comentarios WHERE texto='O clipe Câmera lenta tem uma ótima narrativa.' LIMIT 1), (SELECT id FROM tags WHERE codigo='album_conceitual'));