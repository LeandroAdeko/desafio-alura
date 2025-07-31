-- Tabela de usuários (painel privado)
CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    nome TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    senha_hash TEXT NOT NULL,
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

-- Tabela de comentários
CREATE TABLE IF NOT EXISTS comentarios (
    id UUID PRIMARY KEY,
    texto TEXT NOT NULL,
    categoria TEXT NOT NULL CHECK (categoria IN ('ELOGIO', 'CRÍTICA', 'SUGESTÃO', 'DÚVIDA', 'SPAM')),
    confianca FLOAT CHECK (confianca BETWEEN 0 AND 1),
    origem TEXT,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    artista_id INTEGER REFERENCES artistas(id),
    album_id INTEGER REFERENCES albuns(id),
    clipe_id INTEGER REFERENCES clipes(id),
    show_id INTEGER REFERENCES shows(id)
);

-- Tabela N:N entre comentários e tags
CREATE TABLE IF NOT EXISTS comentario_tags (
    comentario_id UUID REFERENCES comentarios(id) ON DELETE CASCADE,
    tag_id INTEGER REFERENCES tags(id),
    PRIMARY KEY (comentario_id, tag_id)
);

-- Tabela de resumos semanais
CREATE TABLE IF NOT EXISTS resumos_semanais (
    id SERIAL PRIMARY KEY,
    semana_ref DATE NOT NULL,
    texto_resumo TEXT NOT NULL,
    enviado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de avaliações do modelo
CREATE TABLE IF NOT EXISTS avaliacoes_modelo (
    id SERIAL PRIMARY KEY,
    data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    recall_spam FLOAT,
    f1_macro FLOAT,
    acuracia_total FLOAT,
    passou_threshold BOOLEAN
);


-- Insert de informações

-- Artistas
INSERT INTO artistas (nome) VALUES
  ('BaianaSystem'),
  ('Edson Gomes'),
  ('Djavan'),
  ('Melly'),
  ('Vandal'),
  ('Pablo'),
  ('Nara Costa'),
  ('Don L')
ON CONFLICT (nome) DO NOTHING;

-- Albuns
INSERT INTO albuns (nome, lancamento, artista_id) VALUES 
  ('O Mundo Dá Voltas', '2024-03-01', (SELECT id FROM artistas WHERE nome='BaianaSystem')),
  ('Mundo Moderno', '2022-01-01', (SELECT id FROM artistas WHERE nome='BaianaSystem')),

  ('Ao Vivo em Ipiaú', '2024-01-01', (SELECT id FROM artistas WHERE nome='Edson Gomes')),
  ('MPB em Movimento - Salvador (Ao Vivo)', '2024-06-01', (SELECT id FROM artistas WHERE nome='Edson Gomes')),

  ('Origem', '2024-01-01', (SELECT id FROM artistas WHERE nome='Djavan')),
  ('D (Ao Vivo em Maceió)', '2024-01-01', (SELECT id FROM artistas WHERE nome='Djavan')),

  ('Amaríssima', '2024-04-01', (SELECT id FROM artistas WHERE nome='Melly')),

  ('Letrado Baiano', '2024-05-01', (SELECT id FROM artistas WHERE nome='Vandal')),
  ('Cobra Criada / Bicho Solto', '2025-01-01', (SELECT id FROM artistas WHERE nome='Vandal')),

  ('Pablo 20 Anos', '2024-09-27', (SELECT id FROM artistas WHERE nome='Pablo')),

  ('Romântica, Vol. 18', '2024-01-01', (SELECT id FROM artistas WHERE nome='Nara Costa')),
  ('Tbt da Rainha', '2025-01-01', (SELECT id FROM artistas WHERE nome='Nara Costa')),

  ('CARO Vapor II', '2025-06-26', (SELECT id FROM artistas WHERE nome='Don L'));

-- Clipes
INSERT INTO clipes (nome, artista_id) VALUES
  ('Paredão Patuscada', (SELECT id FROM artistas WHERE nome='BaianaSystem')),
  ('O Mundo Dá Voltas (Álbum Visual)', (SELECT id FROM artistas WHERE nome='BaianaSystem')),

  ('Árvore (Ao Vivo no MPB em Movimento 2024)', (SELECT id FROM artistas WHERE nome='Edson Gomes')),

  ('North Sea Jazz 2024 - Show Completo', (SELECT id FROM artistas WHERE nome='Djavan')),

  ('Paraíso', (SELECT id FROM artistas WHERE nome='Melly')),
  ('Derreter & Suar', (SELECT id FROM artistas WHERE nome='Melly')),

  ('Letrado Baiano', (SELECT id FROM artistas WHERE nome='Vandal')),
  ('Feira do Rolo', (SELECT id FROM artistas WHERE nome='Vandal')),

  ('Neosa, Te Love', (SELECT id FROM artistas WHERE nome='Pablo')),
  ('Imprevistos (Bodega do Pablo)', (SELECT id FROM artistas WHERE nome='Pablo')),

  ('O Que É O Que É - Show Gonzaguinha 70 anos', (SELECT id FROM artistas WHERE nome='Nara Costa')),

  ('Tudo É Pra Sempre Agora', (SELECT id FROM artistas WHERE nome='Don L'));

-- Shows
INSERT INTO shows (nome, local, data, artista_id) VALUES 
  ('Lollapalooza Brazil', 'Autódromo de Interlagos, São Paulo', '2024-03-22', (SELECT id FROM artistas WHERE nome='BaianaSystem')),

  ('São João É Na Barra', 'Barra, Bahia', '2024-06-24', (SELECT id FROM artistas WHERE nome='Edson Gomes')),
  ('VI Encontro de Raízes', 'Ipiaú, Bahia', '2024-01-01', (SELECT id FROM artistas WHERE nome='Edson Gomes')),

  ('North Sea Jazz Festival', 'Roterdã, Holanda', '2024-07-12', (SELECT id FROM artistas WHERE nome='Djavan')),
  ('Som Brasil Especial Djavan', 'TV / Estúdio', '2024-11-13', (SELECT id FROM artistas WHERE nome='Djavan')),

  ('Lançamento de Amaríssima (evento de divulgação)', 'Salvador, BA', '2024-10-05', (SELECT id FROM artistas WHERE nome='Melly')),

  ('Show 20 Anos de Carreira', 'Rio de Janeiro, RJ', '2025-09-27', (SELECT id FROM artistas WHERE nome='Pablo')),
  ('Ao Vivo em Buerarema', 'Buerarema, BA', '2024-09-16', (SELECT id FROM artistas WHERE nome='Pablo')),

  ('Show Gonzaguinha 70 anos', 'local não especificado (evento comemorativo)', '2024-11-01', (SELECT id FROM artistas WHERE nome='Nara Costa')),

  ('Últimos shows da turnê “Roteiro Pra Ainouz Vol. 2”', 'Casa Natura Musical, São Paulo', '2025-03-26', (SELECT id FROM artistas WHERE nome='Don L'));
