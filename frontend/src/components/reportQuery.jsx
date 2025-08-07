
const reportQueries = {
  
  albunsDoArtista: `
  SELECT
    id,
    nome,
    lancamento
  FROM albuns
  WHERE artista_id = $1;`,
  
  showsDoArtista: `SELECT
    id,
    nome,
    local,
    data
  FROM shows
  WHERE artista_id = $1;`,
  
  clipesDoArtista: `
    SELECT
      id,
      nome
    FROM clipes
    WHERE artista_id = $1;`,
  
  todosComentarios: `
  SELECT
  c.id as comentario_id,
  c.texto AS comentario_texto,
  c.categoria AS comentario_categoria,
  c.confianca AS comentario_confianca,
  c.criado_em AS comentario_criado_em,
  STRING_AGG(t.codigo, ',') AS tags_list,
  COALESCE(a.id, al_art.id, s_art.id, cl_art.id) AS artista_id,
  COALESCE(a.nome, al_art.nome, s_art.nome, cl_art.nome) AS artista_nome,
  al.id AS album_id,
  al.nome AS album_nome,
  cl.id AS clipe_id,
  cl.nome AS clipe_nome,
  s.id AS show_id,
  s.nome AS show_nome
FROM comentarios c
LEFT JOIN artistas a ON c.artista_id = a.id
LEFT JOIN albuns al ON c.album_id = al.id
LEFT JOIN artistas al_art ON al.artista_id = al_art.id
LEFT JOIN clipes cl ON c.clipe_id = cl.id
LEFT JOIN artistas cl_art ON cl.artista_id = cl_art.id
LEFT JOIN shows s ON c.show_id = s.id
LEFT JOIN artistas s_art ON s.artista_id = s_art.id
LEFT JOIN comentario_tags ct ON c.id = ct.comentario_id
LEFT JOIN tags t ON ct.tag_id = t.id
GROUP BY c.id, a.id, al.id, al_art.id, cl.id, cl_art.id, s.id, s_art.id
ORDER BY c.criado_em DESC;`
};

export default reportQueries;
